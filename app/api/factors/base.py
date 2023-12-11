import pandas as pd
import plotly.graph_objects as go
from ..universes import Universe
from ... import core


class Factor:
    def __init__(self, universe: Universe) -> None:
        self.universe = universe
        self.periods = 1
        self.quantiles = 5
        self.zero_aware = False

    @classmethod
    def create(cls, universe: str = "GlobalAllo") -> "Factor":
        return cls(universe=Universe(universe))

    def __str__(self) -> str:
        return f"{str(self.universe)}.Factor.{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{repr(self.universe)}.Factor.{self.__class__.__name__}"

    def fit(self) -> pd.DataFrame:
        raise NotImplementedError("Must Implement `fit` method.")

    @property
    def values(self) -> pd.DataFrame:
        return self.fit().dropna(how="all")

    @property
    def quantilized(self) -> pd.DataFrame:
        return self.values.apply(
            core.to_quantile,
            axis=1,
            quantiles=self.quantiles,
            zero_aware=self.zero_aware,
        )

    def weights(self) -> pd.DataFrame:
        quantilized = self.quantilized
        return quantilized.apply(core.sum_to_one, axis=1)

    def quantile_performances(self) -> pd.DataFrame:
        quantilized = self.quantilized
        pri_return = self.universe.tr_last.pct_change()
        performances = [self.universe.performance]
        for quantile in [1, self.quantiles]:
            masked = quantilized.applymap(lambda x: 0 if x != quantile else x).shift(1)
            weight = masked.apply(core.sum_to_one, axis=1)
            q_return = pri_return.multiply(weight).sum(axis=1)
            performance = q_return.add(1).cumprod()
            performance.name = f"Q{quantile}"
            performances.append(performance)
        return pd.concat(performances, axis=1)

    def performance(self) -> pd.DataFrame:
        pct_change = self.quantile_performances().pct_change()
        ts_returns = pct_change.iloc[:, -1] - pct_change.iloc[:, 0]
        alpha_ts = ts_returns.fillna(0).add(1).cumprod()
        alpha_ts.name = "TimeSeries"

        cs_returns = pct_change.iloc[:, -1] - pct_change.iloc[:, 1]
        alpha_cs = cs_returns.fillna(0).add(1).cumprod()
        alpha_cs.name = "CrossSection"

        return pd.concat([alpha_ts, alpha_cs], axis=1)

    def plot(self) -> None:
        fig = go.Figure()
        performances = self.quantile_performances()

        for quantile, performance in performances.items():
            fig.add_trace(
                go.Scatter(x=performance.index, y=performance.values, name=quantile)
            )

        fig.update_layout(
            title=dict(
                text="Factor Performane (Quantile)",
                font=dict(family="Arial", size=12, color="black"),
            ),
            yaxis=dict(overlaying="y", side="right", type="log"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            hovermode="x unified",
        )
        return fig


class PxMom6M(Factor):
    def fit(self) -> pd.DataFrame:
        return self.universe.tr_last.apply(core.MO, window=21 * 6)


class LowVolatility(Factor):
    def fit(self) -> pd.DataFrame:
        px = self.universe.tr_last
        out = px.apply(core.log_return)
        out = out.apply(core.STDEV, window=21 * 12) * (-1)
        return out


import numpy as np
import pandas as pd


class Momentum(Factor):
    def fit(self) -> pd.DataFrame:
        """
        Calculate the Momentum factor based on the price data.

        Returns:
            pd.DataFrame: Momentum factor with scores applied.
        """
        px = self.universe.tr_last

        def momentum(px: pd.DataFrame, months: int) -> pd.DataFrame:
            """
            Calculate the momentum factor for a specific window size.

            Args:
                px (pd.DataFrame): Price data.
                months (int): Number of months for the momentum calculation.

            Returns:
                pd.DataFrame: Momentum factor for the specified window size.
            """
            out = px.apply(core.MO, window=21**months)
            out = out.apply(core.StandardScaler, axis=1)
            out = out.apply(core.Winsorize, low=-3, upper=3)
            return out

        factor = np.mean([px.apply(momentum, months=m) for m in (6, 12)], axis=0)

        def to_score(x) -> float:
            """
            Convert momentum factor values to scores.

            Args:
                x: Value of the momentum factor.

            Returns:
                float: Score based on the momentum factor value.
            """
            if x > 0:
                return 1 + x
            elif x < 0:
                return (1 - x) ** (-1)
            else:
                return 0

        return factor.applymap(to_score)
