from typing import Optional, List, Callable, Dict, Union, List
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
    def from_code(
        cls,
        code: str,
    ) -> "Universe":
        return cls(cls.UNIVERSE[code])

    def __init__(
        self,
        assets: List[str],
    ) -> None:
        self.assets = sorted(assets)
        self.num_assets = len(self.assets)
        self.factors = {}

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
        func: Callable[..., pd.DataFrame],
        periods: Union[int, List[int]] = 1,
        quantiles: int = 5,
        zero_aware: int = 0,
    ) -> "Universe":
        """add factor"""
        key = f"{func.__name__}(q:{quantiles}; za:{zero_aware})"
        prices = self.get_prices()
        if key in self.factors:
            weights = self.factors[key]["weights"]
            performance = self.factors[key]["performance"]
        else:
            factors = func(self).reindex(index=prices.index, columns=prices.columns)
            weights = factors.apply(
                core.to_quantile, axis=1, quantiles=quantiles, zero_aware=zero_aware
            ).apply(core.sum_to_one, axis=1)
            performance = pd.DataFrame()
            self.factors.update({key: {"factors": factors, "weights": weights}})
        for p in [periods] if isinstance(periods, int) else periods:
            if p in performance.columns:
                continue
            fwd_return = prices.apply(core.mean_fwd_return, periods=p)
            fwd_return = fwd_return.apply(core.demeaned, axis=1)
            fac_return = fwd_return.multiply(weights).dropna(how="all").sum(axis=1)
            perf = fac_return.add(1).cumprod()
            perf.name = p
            performance = pd.concat([performance, perf], axis=1)
        self.factors[key].update({"performance": performance.sort_index(axis=1)})
        return self






# class Factor:
#     def __init__(
#         self,
#         func: Callable[..., pd.DataFrame],
#         universe: Universe,
#         periods: int = 1,
#         quantiles: int = 5,
#         zero_aware: bool = False,
#     ) -> None:
#         self.factors = func(universe)
#         self.periods = periods
#         self.quantiles = quantiles
#         self.zero_aware = zero_aware

#     def weights(self) -> pd.DataFrame:
#         weights = self.factors.apply(
#             core.to_quantile,
#             axis=1,
#             quantiles=self.quantiles,
#             zero_aware=self.zero_aware,
#         ).apply(core.sum_to_one, axis=1)
#         return weights

#     @property
#     def fwd_return(self) -> pd.DataFrame:
#         fwd_return = self.prices.apply(
#             core.pri_return, axis=0, forward=True, periods=self.periods
#         )
#         fwd_return = fwd_return / self.periods
#         fwd_return = fwd_return.apply(core.demeaned, axis=1)
#         return fwd_return

#     @property
#     def performance(self) -> pd.Series:
#         performance = (
#             self.fwd_return.multiply(self.weights).dropna(how="all").sum(axis=1)
#         )
#         return performance.add(1).cumprod()

#     @property
#     def information_coefficient(self) -> pd.Series:
#         key = "information_coefficient"
#         if key in self:
#             out = pd.DataFrame(self[key])
#             return out.set_index(out.columns[0]).squeeze()
#         from scipy.stats import spearmanr

#         ic = {}
#         for (idx1, row1), (_, row2) in zip(
#             self.fwd_return.iterrows(), self.factors.iterrows()
#         ):
#             try:
#                 ic[idx1] = spearmanr(a=row1, b=row2, nan_policy="omit")[0]
#             except ValueError:
#                 pass
#         ic = pd.Series(ic).dropna()
#         self[key] = ic.reset_index().to_dict("records")
#         return ic

#     def to_signature(self):
#         factors = self.factor

#         return {
#             "periods": self.periods,
#             "quantiles": self.quantiles,
#             "zero_aware": self.zero_aware,
#             "weights": self.weights.reset_index().to_dict("records"),
#             "performance": self.performance.reset_index().to_dict("records"),
#         }
