from typing import Tuple
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ..universes import Universe
from ...core import perf
from ...core import MACD, SMA
from ...db import get_vix
from ..utils import Cache


class Signal:
    def __init__(self, universe: Universe) -> None:
        self.universe = universe

    @classmethod
    def create(cls, universe: str = "GlobalAllo") -> "Signal":
        return cls(Universe(universe))

    def fit(self) -> pd.Series:
        raise NotImplementedError("Must Implement `fit` method.")

    @property
    def values(self) -> pd.Series:
        signal = self.fit().dropna()
        signal.name = "Signal"
        return signal

    @property
    def performance(self) -> pd.Series:
        pri_returns = perf.pri_return(self.universe.performance)
        weights = self.values.reindex(pri_returns.index).ffill().dropna().shift(1).fillna(0)
        return pri_returns.multiply(weights, axis=0).add(1).cumprod().dropna()


    def plot(self, display_mode_bar: bool = False) -> go.Figure:
        """
        Generate a Plotly figure with subplots for Signal, Market, and Performance.
        """
        fig = make_subplots(rows=1, cols=2)

        # Obtain data
        signal = self.values
        perfor = self.performance
        market = self.universe.performance.reindex(perfor.index)
        market = market / market.dropna().iloc[0]

        # Add traces to the subplots with specified rows and columns

        fig.add_trace(
            go.Scatter(x=signal.index, y=signal.values, name=signal.name), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=market.index, y=market.values, name="Market", yaxis="y2"),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Scatter(x=perfor.index, y=perfor.values, name="Performance", yaxis="y2"),
            row=1,
            col=2,
        )

        # Update layout
        fig.update_layout(
            title=dict(
                text="Signal Performance (Asset Class)",
                font=dict(family="Arial", size=12, color="black"),
            ),
            yaxis=dict(tickformat=".0%"),
            yaxis2=dict(overlaying="y", side="right", type="log"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            hovermode="x unified",
        )

        return fig


import pandas as pd
from ...core import StandardScaler
from ...db import get_oecd_us_lei


class OecdUsCli(Signal):
    """
    Why OECD US Composite Leading Indicators?
        The paramount driver of the market is undoubtedly investor expectations.
        Market rallies are often fueled by optimistic projections of economic
        improvements, rather than when the economy is already at its peak.
        Consequently, utilizing a forward-looking indicator with comprehensive
        economic coverage becomes highly relevant.

        The OECD US Composite Leading Indicators present a compelling choice
        in this regard. By encompassing a diverse array of economic indicators
        and data, these indicators offer valuable insights into the future
        direction of the economy. As a result, they serve as a crucial tool
        for investors seeking to anticipate market trends and make informed decisions.

        In summary, opting for the OECD US Composite Leading Indicators is a
        logical and strategic move, given their ability to provide early signals
        of economic shifts, which can substantially enhance investment strategies
        and outcomes.
    """

    def fit(self) -> pd.Series:
        data = get_oecd_us_lei().resample("M").last() - 100
        data.index = data.index + pd.DateOffset(months=1)
        data = data.diff().diff()
        scaler = data.rolling(12 * 5, min_periods=12).apply(
            lambda args: StandardScaler(args).iloc[-1],
        )
        scaler = scaler.divide(2).clip(-1, 1)
        return scaler + 1


class CapacityUtilization(Signal):
    def fit(self) -> pd.Series:
        from ...db import get_data

        data = get_data("TCU", "PX_LAST")["TCU"]
        return -MACD(data)


class SilverGoldRatio(Signal):
    def fit(self) -> pd.Series:
        import yfinance as yf

        pxs = yf.download(tickers="GC=F, SI=F")["Adj Close"].ffill()
        gld = pxs["GC=F"]
        sil = pxs["SI=F"]
        ind = sil / gld
        data = MACD(ind)
        roll = data.rolling(252)
        mu, vo = roll.mean(), roll.std()
        data = (data - mu) / vo / 2
        data = data.clip(-1, 1)
        return data + 1


class VixMomentum(Signal):
    def fit(self) -> pd.Series:
        from ...core import MinMaxScaler

        def map(x):
            if x > 25:
                return 2
            if x < 15:
                return 1
            else:
                return 0

        data = get_vix().apply(map)
        return data


class AudCadMom(Signal):
    def fit(self) -> pd.Series:
        import yfinance as yf

        data = yf.download("AUDCAD=X")["Adj Close"]
        data = SMA(data, 20)
        roll = data.rolling(252)
        mu, vo = roll.mean(), roll.std()
        data = (data - mu) / vo / 2
        data = data.clip(-1, 1)
        return data + 1
