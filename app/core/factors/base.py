import numpy as np
import pandas as pd
from app.core import stats
from app.core import universes


class Factor:
    def __init__(self, universe: "universes.Universe") -> None:
        self.__data__ = {}
        self.universe = universe
        self.data = pd.DataFrame()
        self.weights = pd.DataFrame()

    def fit(self) -> "Factor":
        raise NotImplementedError("Must implement fit method.")

    def to_weights(self) -> pd.DataFrame:
        name = "weights"
        if name not in self.__data__:
            rank = self.data.rank(axis=1)
            weights = rank.div(rank.sum(axis=1), axis=0).sub(
                1 / rank.max(axis=1), axis=0
            )
            weights = weights.shift(1).dropna(thresh=2)
            self.__data__[name] = weights
        return self.__data__[name]

    def to_performance(self, periods: int = 21, commission=10) -> pd.Series:
        name = "performance"
        weights = self.to_weights()
        if name not in self.__data__:
            print("update performance")
            prices = self.universe.get_prices().loc[weights.index[0] :]
            log_return = (
                stats.log_return(prices, periods=periods, forward=True) / periods
            )
            p_log_return = log_return.mul(weights).dropna(how="all").sum(axis=1)
            turnover = weights.diff().abs().sum(axis=1) * commission / 10_0000
            p_log_return = p_log_return - turnover.apply(np.log1p)
            out = p_log_return.cumsum().apply(np.exp)
            out.name = self.__class__.__name__
            out = out.dropna()
            self.__data__[name] = out
        return self.__data__[name]

    def information_coefficient(self) -> pd.Series:
        name = "ic"
        if name not in self.__data__:
            pri = self.universe.get_prices()
            fwd = stats.pri_return(pri, periods=21, forward=True)
            ic = (
                stats.information_coefficient(self.to_weights(), fwd)
                .dropna()
                .rolling(252)
                .mean()
            )

            self.__data__[name] = ic
        return self.__data__[name]
