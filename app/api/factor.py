from typing import Type, Dict
import numpy as np
import pandas as pd
from .universe import Universe
from .regime import UsLei, VolState, AbsorptionRatio


from .. import core


class Factor:
    def __init__(self, universe: Universe) -> None:
        self.universe = universe
        self.data = self.fit()

    def fit(self) -> pd.DataFrame:
        raise NotImplementedError("Must implement `fit` method for `Factor` class.")

    @property
    def weights(self) -> pd.DataFrame:
        rank = self.data.rank(axis=1)
        weights = rank.div(rank.sum(axis=1), axis=0)
        weights = weights.sub(1 / rank.max(axis=1), axis=0)
        weights = weights.shift(1).dropna(thresh=2)
        return weights

    @property
    def information_coefficient(self) -> pd.Series:
        pri = self.universe.get_prices()
        fwd = core.pri_return(pri, periods=21, forward=True)
        ic = (
            core.information_coefficient(self.weights, fwd).dropna().rolling(252).mean()
        )
        return ic

    @property
    def turnover(self) -> pd.Series:
        out = self.weights.diff().abs().sum(axis=1)
        out.iloc[0] = self.weights.iloc[0].abs().sum()
        return out

    def to_performance(self, periods: int = 21, commission=10) -> pd.Series:
        prices = self.universe.get_prices().loc[self.weights.index[0] :]
        log_return = core.log_return(prices, periods=periods, forward=True)
        log_return = log_return / periods
        p_log_return = log_return.mul(self.weights).dropna(how="all").sum(axis=1)
        total_cost = self.turnover * commission / 10_000
        p_log_return = p_log_return - total_cost.apply(np.log1p)
        out = p_log_return.cumsum().apply(np.exp)
        out.name = self.__class__.__name__
        out = out.dropna()
        return out


class PxMom1M(Factor):
    periods = 1 * 21

    def fit(self) -> pd.DataFrame:
        return core.pri_return(data=self.universe.get_prices(), periods=self.periods)


class PxMom2M(PxMom1M):
    periods = 2 * 21


class PxMom3M(PxMom1M):
    periods = 3 * 21


class PxMom4M(PxMom1M):
    periods = 4 * 21


class PxMom5M(PxMom1M):
    periods = 5 * 21


class PxMom6M(PxMom1M):
    periods = 6 * 21


class PxMom7M(PxMom1M):
    periods = 7 * 21


class PxMom8M(PxMom1M):
    periods = 8 * 21


class PxMom9M(PxMom1M):
    periods = 9 * 21


class PxMom10M(PxMom1M):
    periods = 10 * 21


class PxMom11M(PxMom1M):
    periods = 11 * 21


class PxMom12M(PxMom1M):
    periods = 12 * 21


class PxMom18M(PxMom1M):
    periods = 18 * 21


class PxMom24M(PxMom1M):
    periods = 24 * 21


class PxMom36M(PxMom1M):
    periods = 36 * 21


class PxRev1M(Factor):
    periods = 0 * 21
    reversal = 1 * 21

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        mom = core.log_return(prices, periods=self.periods)
        rev = core.log_return(prices, periods=self.reversal)
        return (mom - rev).apply(np.exp) - 1


class PxRev6M1M(PxRev1M):
    periods = 6 * 21
    reversal = 1 * 21


class PxRev12M1M(PxRev1M):
    periods = 12 * 21
    reversal = 1 * 21


class PxRev18M1M(PxRev1M):
    periods = 18 * 21
    reversal = 1 * 21


class PxRev6M2M(PxRev1M):
    periods = 6 * 21
    reversal = 2 * 21


class PxRev12M2M(PxRev1M):
    periods = 12 * 21
    reversal = 2 * 21


class PxRev18M2M(PxRev1M):
    periods = 18 * 21
    reversal = 2 * 21


class VCV1M(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        volume = self.universe.get_volumes()
        mean = volume.rolling(self.months * 21).mean()
        std = volume.rolling(self.months * 21).std()
        return -std / mean


class VCV3M(VCV1M):
    months = 3


class VCV6M(VCV1M):
    months = 6


class VCV9M(VCV1M):
    months = 9


class VCV12M(VCV1M):
    months = 12


class PxVol1M(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        pri_return = prices.pct_change()
        return pri_return.rolling(21 * self.months).std()


class PxVol3M(PxVol1M):
    months = 3


class UsLei5Y(Factor):
    years = 5
    min_years = 1
    regime = UsLei

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        pri_return = core.pri_return(prices, periods=1, forward=True)
        states = self.regime().fit().states.reindex(pri_return.index).ffill()
        holder = pd.DataFrame(columns=pri_return.columns, index=pri_return.index)
        for state in self.regime.__state__:
            fil = states != state
            masked_data = pri_return.where(fil, np.nan)
            exp_returns = masked_data.rolling(
                252 * self.years, min_periods=252 * self.min_years
            ).mean()
            holder.update(exp_returns.where(fil, np.nan))
        return holder


class UsLei10Y(UsLei5Y):
    years = 10
    min_years = 1
    regime = UsLei


class VolState5Y(UsLei5Y):
    years = 5
    min_years = 1
    regime = VolState


class Absorption1Y(UsLei5Y):
    years = 5
    min_years = 1
    regime = AbsorptionRatio


class PxRsi50(Factor):
    periods: int = 50

    def fit(self) -> pd.DataFrame:
        prices = self.universe.get_prices()
        rsi = core.RSI(prices, self.periods).clip(lower=0.2, upper=0.8)
        return rsi


class PxBBand50(Factor):
    periods: int = 50

    def fit(self) -> pd.DataFrame:
        return core.BBand(self.universe.get_prices(), self.periods)


class MultiFactors:
    factors: Dict[str, Type[Factor]] = {
        "PxMom1M": PxMom1M,
        "PxMom2M": PxMom2M,
        "PxMom3M": PxMom3M,
        "PxMom4M": PxMom4M,
        "PxMom5M": PxMom5M,
        "PxMom6M": PxMom6M,
        "PxMom7M": PxMom7M,
        "PxMom8M": PxMom8M,
        "PxMom9M": PxMom9M,
        "PxMom10M": PxMom10M,
        "PxMom11M": PxMom11M,
        "PxMom12M": PxMom12M,
        "PxMom18M": PxMom18M,
        "PxMom24M": PxMom24M,
        "PxMom36M": PxMom36M,
        "VCV1M": VCV1M,
        "VCV3M": VCV3M,
        "VCV6M": VCV6M,
        "VCV9M": VCV9M,
        "VCV12M": VCV12M,
        "PxVol1M": PxVol1M,
        "PxVol3M": PxVol3M,
        "PxRsi50": PxRsi50,
        "UsLei5Y": UsLei5Y,
        "UsLei10Y": UsLei10Y,
        "VolState5Y": VolState5Y,
        # "Absorption1Y": Absorption1Y,
        "PxBBand50" : PxBBand50,
    }

    def __init__(self, universe: Universe) -> None:
        self.universe = universe

    def to_performance(self, periods: int = 21, commission: int = 10) -> pd.DataFrame:
        performances = []
        for f_name, f_cls in self.factors.items():
            f_self = f_cls(universe=self.universe)
            performance = f_self.to_performance(periods, commission)
            performance.name = f_name
            performances.append(performance)
        return pd.concat(performances, axis=1)
