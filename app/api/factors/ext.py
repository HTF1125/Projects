"""ROBERT"""
import numpy as np
import pandas as pd
from app.core import stats
from app.api.base import Factor

from typing import Type
import numpy as np
import pandas as pd
from app.core import stats
from app.api import regimes



class PxMom(Factor):
    periods: int = 1

    def fit(self) -> pd.DataFrame:
        return stats.pri_return(data=self.universe.get_prices(), periods=self.periods)


class PxRev(Factor):
    periods: int = 1
    reversal: int = 1

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        mom = stats.log_return(prices, periods=self.periods)
        rev = stats.log_return(prices, periods=self.reversal)
        return (mom - rev).apply(np.exp) - 1


class PxMom1M(PxMom):
    periods = 1 * 21


class PxMom2M(PxMom):
    periods = 2 * 21


class PxMom3M(PxMom):
    periods = 3 * 21


class PxMom4M(PxMom):
    periods = 4 * 21


class PxMom5M(PxMom):
    periods = 5 * 21


class PxMom6M(PxMom):
    periods = 6 * 21


class PxMom7M(PxMom):
    periods = 7 * 21


class PxMom8M(PxMom):
    periods = 8 * 21


class PxMom9M(PxMom):
    periods = 9 * 21


class PxMom10M(PxMom):
    periods = 10 * 21


class PxMom11M(PxMom):
    periods = 11 * 21


class PxMom12M(PxMom):
    periods = 12 * 21


class PxMom24M(PxMom):
    periods = 24 * 21


class PxMom36M(PxMom):
    periods = 36 * 21


class PxRev1M(PxRev):
    periods = 0 * 21
    reversal = 1 * 21


class PxRev6M1M(PxRev):
    periods = 6 * 21
    reversal = 1 * 21


class PxRev12M1M(PxRev):
    periods = 12 * 21
    reversal = 1 * 21


class PxRev18M1M(PxRev):
    periods = 18 * 21
    reversal = 1 * 21


class PxRev6M2M(PxRev):
    periods = 6 * 21
    reversal = 2 * 21


class PxRev12M2M(PxRev):
    periods = 12 * 21
    reversal = 2 * 21


class PxRev18M2M(PxRev):
    periods = 18 * 21
    reversal = 2 * 21


class VCV(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        volume = self.universe.get_volumes()
        mean = volume.rolling(self.months * 21).mean()
        std = volume.rolling(self.months * 21).std()
        return -std / mean


class VCV1M(VCV):
    months = 1


class VCV3M(VCV):
    months = 3


class VCV6M(VCV):
    months = 6


class VCV12M(VCV):
    months = 12


class PxVol(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        pri_return = prices.pct_change()
        return pri_return.rolling(21 * self.months).std()


class PxVol1M(PxVol):
    months = 1


class PxVol3M(PxVol):
    months = 3


class PxRSI10(Factor):
    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        rsi = stats.RSI(prices, 50).clip(lower=0.2, upper=0.8).mul(-1)
        return rsi


class RegimeFactor(Factor):
    years: int = 5
    min_years = 1
    regime: Type[regimes.Regime]

    def fit(self) -> pd.DataFrame:
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
        return holder


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
