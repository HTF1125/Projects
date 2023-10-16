import time
import numpy as np
import pandas as pd
from app.core import stats
from app.core import universes


class Factor:

    def __init__(self, universe: "universes.Universe") -> None:
        self.universe = universe
        self.data = pd.DataFrame()
        self.cache = {}

    def fit(self) -> "Factor":
        raise NotImplementedError("Must implement fit method.")

    def to_weights(self) -> pd.DataFrame:
        name = "weights"
        if name not in self.cache:
            rank = self.data.rank(axis=1)
            weights = rank.div(rank.sum(axis=1), axis=0).sub(
                1 / rank.max(axis=1), axis=0
            )
            weights = weights.shift(1).dropna(thresh=2)
            self.cache[name] = weights
        return self.cache[name]

    def to_performance(self, periods: int = 21, commission=10) -> pd.Series:
        name = "performance"
        weights = self.to_weights()
        if name not in self.cache:
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
            self.cache[name] = out
        return self.cache[name]

    def information_coefficient(self) -> pd.Series:
        name = "ic"
        if name not in self.cache:
            pri = self.universe.get_prices()
            fwd = stats.pri_return(pri, periods=21, forward=True)
            ic = (
                stats.information_coefficient(self.to_weights(), fwd)
                .dropna()
                .rolling(252)
                .mean()
            )

            self.cache[name] = ic
        return self.cache[name]
