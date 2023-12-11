
"""



"""


import pandas as pd
from .base import Factor


class MeanReversion1M(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        return self.universe.tr_last.pct_change(self.months * 21) * (-1)