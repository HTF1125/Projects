from typing import Optional, List
import numpy as np
import pandas as pd
from .. import core
from .. import db


class Universe:
    UNIVERSE = {
        "UsSectors": [
            "XLC",
            "XLY",
            "XLP",
            "XLE",
            "XLF",
            "XLV",
            "XLI",
            "XLB",
            "XLK",
            "XLU",
            "XLRE",
        ],
        "GlobalAllo": [
            "SPY",
            "AGG",
            "TLT",
            "GSG",
            "TIP",
            "IVV",
            "GLD",
        ],
    }

    @classmethod
    def from_code(cls, code: str) -> "Universe":
        return cls(cls.UNIVERSE[code])

    def __init__(self, assets: List[str]) -> None:
        self.assets = sorted(assets)
        self.num_assets = len(self.assets)

    def get_prices(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        # get prices
        data = db.get_data(tickers=", ".join(self.assets), features="TR_INDEX")
        data = data.reindex(columns=self.assets)
        if date is not None:
            data = data.loc[:date].dropna(how="all", axis=1)
        return data

    def get_volumes(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        # get volumes
        data = db.get_data(tickers=", ".join(self.assets), features="PX_VOLUME")
        data = data.reindex(columns=self.assets)
        if date is not None:
            data = data.loc[:date].dropna(how="all", axis=1)
        return data

    def cov(
        self, method: str = "sample", date: Optional[pd.Timestamp] = None
    ) -> pd.DataFrame:
        data = self.get_prices(date=date).apply(core.perf.log_return, periods=1)
        S = np.zeros((self.num_assets, self.num_assets))
        for i in range(self.num_assets):
            for j in range(i, self.num_assets):
                S[i, j] = S[j, i] = core.stat.empirical_cov(
                    data.iloc[:, i], data.iloc[:, j]
                )
        data = pd.DataFrame(data=S, columns=self.assets, index=self.assets)
        return data

    def expectation(
        self,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.Series:
        return self.get_prices(date=date).apply(core.perf.log_return).mean() * 252

    def covariance(
        self,
        window: int = 252 * 3,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        return self.get_prices(date=date).apply(core.perf.log_return).iloc[-window:].cov() * 252

    def correlation(
        self,
        window: int = 252 * 3,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        return self.get_prices(date=date).apply(core.perf.log_return).iloc[-window:].corr()

    def solve(
        self,
        risk_free: float = 0.0,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        sum_weight: float = 1.0,
    ):
        from scipy.optimize import minimize

        constratins = [
            {"type": "ineq", "fun": lambda w: w - min_weight},
            {"type": "ineq", "fun": lambda w: max_weight - w},
            {"type": "eq", "fun": lambda w: np.sum(w) - sum_weight},
        ]

        x0 = np.ones(len(self.assets)) / len(self.assets)

        problem = minimize(
            fun=lambda x: self.expectation().dot(x),
            x0=x0,
            method="SLSQP",
            constraints=constratins,
        )
        if problem.success:
            data = problem.x + 1e-16
            w = pd.Series(data=data, index=self.assets, name="weights")
            return w.round(6)
        return pd.Series({})
