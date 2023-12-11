"""
"""
from typing import Optional
import numpy as np
import pandas as pd
from ...db import get_data, get_assets
from ...core import stat, perf


class Universe:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.assets = get_assets(universe=self.ticker)
        self.n_assets = len(self.assets)

    @property
    def tr_last(self) -> pd.DataFrame:
        return get_data(tickers=self.assets, fields="TR_LAST")

    @property
    def px_volume(self) -> pd.DataFrame:
        return get_data(tickers=self.assets, fields="PX_VOLUME")

    @property
    def performance(self) -> pd.Series:
        performance = self.tr_last.pct_change().mean(axis=1).fillna(0).add(1).cumprod()
        performance.name = "Market Performance"
        return performance

    def cov(
        self,
        method: str = "sample",
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        if method == "sample":
            data = self.tr_last
            if date:
                data = data.loc[:date]
            data = data.apply(perf.log_return, periods=1)
            S = np.zeros((self.n_assets, self.n_assets))
            for i in range(self.n_assets):
                for j in range(i, self.n_assets):
                    S[i, j] = S[j, i] = stat.empirical_cov(
                        data.iloc[:, i], data.iloc[:, j]
                    )
            data = pd.DataFrame(data=S, columns=self.assets, index=self.assets)
            return data
        raise ValueError("Other methods are not implemented.")

    def get_mean_forward_performance(self, periods: int = 1) -> pd.DataFrame:
        return (
            self.performance.apply(
                perf.pri_return,
                periods=periods,
                forward=True,
            )
            / periods
        )
