"""ROBERT"""
import numpy as np
from app.core import stats
from .base import Factor


class PxMom(Factor):
    periods: int = 1

    def fit(self) -> "Factor":
        self.data = stats.pri_return(
            data=self.universe.get_prices(), periods=self.periods
        )
        return self


class PxRev(Factor):
    periods: int = 1
    reversal: int = 1

    def fit(self) -> "Factor":
        prices = self.universe.get_prices()
        mom = stats.log_return(prices, periods=self.periods)
        rev = stats.log_return(prices, periods=self.reversal)
        self.data = (mom - rev).apply(np.exp) - 1
        return self


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

    def fit(self) -> "Factor":
        volume = self.universe.get_volumes()
        mean = volume.rolling(self.months * 21).mean()
        std = volume.rolling(self.months * 21).std()
        self.data = -std / mean
        return self


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

    def fit(self) -> "Factor":
        prices = self.universe.get_prices()
        pri_return = prices.pct_change()
        self.data = pri_return.rolling(21 * self.months).std()
        return self


class PxVol1M(PxVol):
    months = 1


class PxVol3M(PxVol):
    months = 3


class PxRSI10(Factor):
    def fit(self) -> "Factor":
        prices = self.universe.get_prices()
        rsi = stats.RSI(prices, 50).clip(lower=0.2, upper=0.8).mul(-1)
        self.data = rsi
        return self
