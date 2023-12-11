import pandas as pd
from .base import Factor
from ...core import perf

class MsciLowv(Factor):
    months = 12

    def fit(self) -> pd.DataFrame:
        lot_return = self.universe.tr_last.apply(perf.log_return)
        return lot_return.rolling(21 * self.months).std() * (-1)


class Lowv3M(MsciLowv):
    months = 3


class Lowv6M(MsciLowv):
    months = 6


class Lowv12M(MsciLowv):
    months = 12
