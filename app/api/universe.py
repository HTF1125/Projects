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

    def get_prices(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        # get prices
        data = db.get_prices(tickers=", ".join(self.assets))
        if date is not None:
            data = data.loc[:date].dropna(how="all", axis=1)
        return data

    def get_volumes(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        # get volumes
        data = db.get_volumes(tickers=", ".join(self.assets))
        if date is not None:
            data = data.loc[:date].dropna(how="all", axis=1)
        return data
















    def expectation(
        self,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.Series:
        return core.log_return(self.get_prices(date=date)).mean() * 252

    def covariance(
        self,
        window: int = 252 * 3,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        return core.log_return(self.get_prices(date=date).iloc[-window:]).cov() * 252

    def correlation(
        self,
        window: int = 252 * 3,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        return core.log_return(self.get_prices(date=date).iloc[-window:]).corr()

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
