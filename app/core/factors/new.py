"""ROBERT"""
from typing import Type
import numpy as np
import pandas as pd
from app.core import stats, regimes
from .base import Factor








class RegimeFactor(Factor):
    years: int = 5
    min_years = 1
    regime: Type[regimes.Regime]

    def fit(self) -> "Factor":
        prices = self.universe.get_prices()
        pri_return = stats.pri_return(prices, periods=1, forward=True)
        states = self.regime().fit().states.reindex(pri_return.index).ffill()
        holder = pd.DataFrame(columns=pri_return.columns, index=pri_return.index)
        for state in self.regime.__state__:
            fil = states != state
            masked_data = pri_return.where(fil, np.nan)
            exp_returns = masked_data.rolling(
                252 * self.years, min_periods=252 * self.min_years
            ).mean()
            holder.update(exp_returns.where(fil, np.nan))
        self.data = holder
        return self


class UsLei5Y(RegimeFactor):
    years = 5
    min_years = 1
    regime = regimes.UsLei


class UsLei10Y(RegimeFactor):
    years = 10
    min_years = 1
    regime = regimes.UsLei


class VolState5Y(RegimeFactor):
    years = 5
    min_years = 1
    regime = regimes.VolState
