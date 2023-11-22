from typing import Optional, List, Callable
import numpy as np
import pandas as pd
from .. import core
from .. import db
from .portfolio import Portfolio


class Payload(dict):
    def __missing__(self, key):
        self[key] = Payload()
        return self[key]


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
    def from_code(
        cls,
        code: str,
    ) -> "Universe":
        return cls(cls.UNIVERSE[code])

    def __init__(
        self,
        assets: List[str],
    ) -> None:
        self.payload = Payload()

        self.assets = sorted(assets)
        self.num_assets = len(self.assets)

    def get_prices(
        self,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        data = db.get_data(tickers=", ".join(self.assets), factors="TR_LAST")
        return data

    def get_volumes(
        self,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        data = db.get_data(tickers=", ".join(self.assets), factors="PX_VOLUME")
        return data

    def get_fwd_return(
        self,
        periods: int = 1,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        prices = self.get_prices()
        return prices.apply(core.pri_return, periods=periods, forward=True)

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
        return (
            self.get_prices(date=date).apply(core.perf.log_return).iloc[-window:].cov()
            * 252
        )

    def correlation(
        self,
        window: int = 252 * 3,
        date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        return (
            self.get_prices(date=date).apply(core.perf.log_return).iloc[-window:].corr()
        )

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

    def add_factor(
        self,
        factor: Callable[..., pd.DataFrame],
        quantiles: int = 5,
        commission: int = 10,
        zero_aware: bool = False,
        demean: bool = True,
    ) -> "Universe":
        """add factor"""
        data = factor(self).dropna(thresh=quantiles, axis=1)
        group = data.apply(
            core.to_quantile,
            axis=1,
            quantiles=quantiles,
            zero_aware=zero_aware,
        )
        weights = group.apply(core.sum_to_one, axis=1).dropna(how="all")
        turnover = weights.diff().abs().sum(axis=1)
        fwd_return = self.get_fwd_return(periods=1)
        if demean: fwd_return = fwd_return.apply(core.demeaned, axis=1)
        fac_return = fwd_return.multiply(weights).dropna(how="all").sum(axis=1)
        fac_return = fac_return - turnover * commission / 10_000
        alpha = fac_return.add(1).cumprod()
        alpha.plot()
        return self
