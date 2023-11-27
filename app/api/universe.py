from typing import Optional, List, Callable, Dict, Union, List, Tuple, Set, Type
import numpy as np
import pandas as pd
from .. import core
from .. import db


__instances__ = {}


def get_universe(
    code: Optional[str] = None,
    assets: Optional[List[str]] = None,
) -> "Universe":
    if code:
        assets = Universe.UNIVERSE.get(code)
    if not assets:
        assets = assets
    if assets is None:
        raise ValueError("...")
    key = tuple(sorted(assets))
    if key in __instances__:
        return __instances__[key]
    instance = Universe(assets=key)
    __instances__[key] = instance
    return instance


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
            "GLD",
            "EEM",
        ],
    }

    def __init__(self, assets: Tuple[str, ...]) -> None:
        self.assets = tuple(sorted(assets))
        self.num_assets = len(self.assets)
        self.f = Factors(self)

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


class Factors:
    def __init__(self, universe: Universe) -> None:
        self.universe = universe
        self.items = {}

    # def get_information_coefficient(self, periods: int = 1) -> pd.Series:
    #     if periods in self.ic:
    #         return self.ic[periods]
    #     from scipy.stats import spearmanr

    #     fwd = self.get_fwd_return(periods=periods)
    #     factors = self.factors.reindex(index=fwd.index, columns=fwd.columns)
    #     ic = {}
    #     for (idx1, r1), (_, r2) in zip(fwd.iterrows(), factors.iterrows()):
    #         try:
    #             ic[idx1] = spearmanr(a=r1, b=r2, nan_policy="omit")[0]
    #         except ValueError:
    #             pass
    #     ic = pd.Series(ic, name=periods).dropna()
    #     self.ic = pd.concat([self.ic, ic], axis=1)
    #     self.ic = self.ic.sort_index(axis=1)
    #     return ic

    def append(
        self,
        func: Union[
            str,
            List[str],
            Tuple[str],
            Set[str],
            Callable[..., pd.DataFrame],
            List[Callable[..., pd.DataFrame]],
        ],
        periods: Union[int, List[int]] = 1,
        quantiles: int = 5,
        zero_aware: int = 0,
    ) -> None:
        if isinstance(func, (list, tuple, set)):
            for f in func:
                self.append(
                    f,
                    periods=periods,
                    quantiles=quantiles,
                    zero_aware=zero_aware,
                )
            return

        if isinstance(func, str):
            from . import factor

            func = getattr(factor, func)
            if not isinstance(func, Callable):
                return

        key = f"{func.__name__}(q:{quantiles}; za:{zero_aware})"
        prices = self.universe.get_prices()
        if key in self.items:
            weights = self.items[key]["weights"]
            performance = self.items[key]["performance"]
        else:
            factors = func(self.universe).reindex(
                index=prices.index, columns=prices.columns
            )
            weights = factors.apply(
                core.to_quantile, axis=1, quantiles=quantiles, zero_aware=zero_aware
            ).apply(core.sum_to_one, axis=1)
            performance = pd.DataFrame()
            self.items.update({key: {"factors": factors, "weights": weights}})
        for p in [periods] if isinstance(periods, int) else periods:
            if p in performance.columns:
                continue
            fwd_return = prices.apply(core.mean_fwd_return, periods=p)
            fwd_return = fwd_return.apply(core.demeaned, axis=1)
            fac_return = fwd_return.multiply(weights).dropna(how="all").sum(axis=1)
            perf = fac_return.add(1).cumprod()
            perf.name = p
            performance = pd.concat([performance, perf], axis=1)
        self.items[key].update({"performance": performance.sort_index(axis=1)})

    def plot(self):
        import plotly.graph_objects as go

        fig = go.Figure()
        for key, value in self.items.items():
            performance = value.get("performance")

            if not isinstance(performance, pd.DataFrame):
                continue
            if performance.empty:
                continue
            for p in performance:
                perf = performance[p].dropna()
                indices = np.linspace(0, len(perf.index) - 1, 50, dtype=int)
                perf = perf.iloc[indices].round(2)

                trace = go.Scatter(
                    x=perf.index,
                    y=perf.values,
                    name=f"{key} {p}",
                )
                fig.add_trace(trace=trace)

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend={
                "orientation": "h",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.05,
                "yanchor": "top",
                "itemsizing": "constant",
            },
            yaxis={
                "tickformat": ".2f%",
            },
            margin={
                "t": 0,
                "l": 0,
                "r": 0,
                "b": 0,
            },
        )

        return fig

    def signature(self) -> Dict:
        return {}
