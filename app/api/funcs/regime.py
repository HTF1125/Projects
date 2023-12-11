"""ROBERT"""
import pandas as pd
from app import db, core


class Regime:
    __state__ = ()

    def __init__(self) -> None:
        self.states = pd.Series(dtype=str)

    def fit(self) -> "Regime":
        raise NotImplementedError("...")

    def forward_return_by_state(
        self, prices: pd.DataFrame, periods: int = 21
    ) -> pd.DataFrame:
        forward_return = core.log_return(
            close=prices,
            window=periods,
            forward=True,
        ).multiply(252 / periods)
        forward_return["__state__"] = self.states.reindex(forward_return.index).ffill()
        return forward_return.groupby(by="__state__").mean()


class UsLei(Regime):
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

    __state__ = ("Recovery", "Contraction")

    def fit(self) -> "Regime":
        cli = db.get_oecd_us_lei()
        cli.index = cli.index + pd.DateOffset(months=1)
        rocc = cli.diff().diff().dropna()
        self.states = rocc.map(
            lambda x: self.__state__[0] if x > 0 else self.__state__[1]
        )
        return self


class VolState(Regime):
    __state__ = "NormalVol", "ExtremeVol"

    def fit(self) -> Regime:
        vix = db.get_vix()
        roll = vix.rolling(252 * 5)
        mean = roll.mean()
        std = roll.std()
        score = (vix - mean) / std
        score = score.abs().dropna()
        self.states = score.map(
            lambda x: self.__state__[0] if x < 0.8 else self.__state__[1]
        )
        return self


class AbsorptionRatio(Regime):
    __states__ = ("HighAR", "LowAR")

    def fit(self) -> Regime:
        pxs = db.get_data(
            tickers="SPY, IEF, TLT, EZU, VPL, EEM, GLD, RWR, EMB, TIP, USDKRW, ^N225, ^KS11"
        ).dropna()
        log_return = pxs.apply(core.log_return)
        result = {}
        for i in log_return.resample("M").last().iloc[12:].index:
            exp_ratio = core.get_absorption_ratio(
                log_return.loc[:i].iloc[-252:]
            )
            result[i] = exp_ratio
        result = pd.Series(result)
        result = (result - result.rolling(12).mean()) / result.rolling(12).std()
        result = result.reindex(log_return.index).ffill()
        self.states = result.dropna().map(
            lambda x: self.__states__[0] if x > 0 else self.__states__[1]
        )
        return self
