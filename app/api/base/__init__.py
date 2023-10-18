from typing import Dict, List, Optional, Type, Union
import importlib
import numpy as np
import pandas as pd
import warnings
from app.core import stats
from app import database


class Universe:
    __instances__ = {}
    assets: Dict[str, str]
    factors: Dict[str, "Factor"]

    def __new__(cls, *args, **kwargs):
        instance = cls.__instances__.get(cls.__name__)
        if isinstance(instance, cls):
            return instance
        instance = super().__new__(cls)
        cls.__instances__.update({cls.__name__: instance})
        return instance

    def __init__(self) -> None:
        self.cache = {}
        if not hasattr(self, "assets"):
            self.assets = {}
        if not hasattr(self, "factors"):
            self.factors = {}

    def add_factors(self, *items: Union[str, Type["Factor"]]) -> "Universe":
        from app.api import factors
        for item in items:
            if isinstance(item, str):
                if not item in factors.__all__:
                    warnings.warn(f"factor {item} does not exist.")
                    continue
                item = getattr(factors, item)
            name = item.__name__
            if name not in self.factors:
                factor = item(universe=self)
                self.factors.update({name: factor})
        return self

    def add_assets(self, *items: str) -> "Universe":
        for item in items:
            key = item if isinstance(item, str) else item.__name__
            if key not in self.assets:
                self.assets.update({key: key})
        return self

    def get_prices(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        if "prices" not in self.cache:
            self.cache["prices"] = database.get_prices(tickers=list(self.assets.keys()))
        return self.cache["prices"]

    def get_volumes(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        if "volumes" not in self.cache:
            self.cache["volumes"] = database.get_volumes(
                tickers=list(self.assets.keys())
            )
        return self.cache["volumes"]


class Factor:
    def __init__(self, universe: Optional[Universe] = None) -> None:
        self.cache = {}
        if universe is not None:
            self.universe = universe

    @property
    def universe(self) -> Universe:
        out = self.cache.get("universe")
        if out is None:
            raise ValueError("Must set universe first.")
        if not isinstance(out, Universe):
            raise TypeError("Universe type incorrect.")
        return out

    @universe.setter
    def universe(self, universe: Universe) -> None:
        if not isinstance(universe, Universe):
            warnings.warn("Something wrong with the cached Universe.")
            return
        self.cache.update({"universe": universe})

    @property
    def data(self) -> pd.DataFrame:
        out = self.cache.get("data")
        if out is None:
            data = self.fit()
            if not isinstance(data, pd.DataFrame):
                raise TypeError("fit method must return a dataframe.")
            self.cache.update({"data": data})
            return self.data
        return out

    @property
    def weights(self) -> pd.DataFrame:
        if "weights" not in self.cache:
            rank = self.data.rank(axis=1)
            weights = rank.div(rank.sum(axis=1), axis=0).sub(
                1 / rank.max(axis=1), axis=0
            )
            weights = weights.shift(1).dropna(thresh=2)
            self.cache["weights"] = weights
        return self.cache["weights"]

    def to_performance(self, periods: int = 21, commission=10) -> pd.Series:
        name = "performance"
        if name not in self.cache:
            prices = self.universe.get_prices().loc[self.weights.index[0] :]
            log_return = (
                stats.log_return(prices, periods=periods, forward=True) / periods
            )
            p_log_return = log_return.mul(self.weights).dropna(how="all").sum(axis=1)
            turnover = self.weights.diff().abs().sum(axis=1) * commission / 10_0000
            p_log_return = p_log_return - turnover.apply(np.log1p)
            out = p_log_return.cumsum().apply(np.exp)
            out.name = self.__class__.__name__
            out = out.dropna()
            self.cache[name] = out
        return self.cache[name]

    def fit(self) -> pd.DataFrame:
        raise NotImplementedError("Must implement `fit` method.")

    @property
    def information_coefficient(self) -> pd.Series:
        name = "information_coefficient"
        if name not in self.cache:
            pri = self.universe.get_prices()
            fwd = stats.pri_return(pri, periods=21, forward=True)
            ic = (
                stats.information_coefficient(self.weights, fwd)
                .dropna()
                .rolling(252)
                .mean()
            )

            self.cache[name] = ic
        return self.cache[name]


class Regime:
    __state__ = ()

    def __init__(self) -> None:
        self.states = pd.Series(dtype=str)

    def fit(self) -> "Regime":
        raise NotImplementedError("...")

    def forward_return_by_state(
        self, prices: pd.DataFrame, periods: int = 21
    ) -> pd.DataFrame:
        forward_return = stats.log_return(
            data=prices,
            periods=periods,
            forward=True,
        ).multiply(252 / periods)
        forward_return["__state__"] = self.states.reindex(forward_return.index).ffill()
        return forward_return.groupby(by="state").mean()
