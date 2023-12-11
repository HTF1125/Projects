import pandas as pd
from .base import Factor
from ...core.perf import pri_return
from ...core.stat import StandardScaler, Winsorize
from ...core.tech import MO


class MsciMomt(Factor):
    def fit(self) -> pd.DataFrame:
        """
        Calculate the Momentum factor based on the price data.

        Returns:
            pd.DataFrame: Momentum factor with scores applied.
        """

        def momentum(p: pd.DataFrame, months: int) -> pd.DataFrame:
            """
            Calculate the momentum factor for a specific window size.

            Args:
                px (pd.DataFrame): Price data.
                months (int): Number of months for the momentum calculation.

            Returns:
                pd.DataFrame: Momentum factor for the specified window size.
            """
            out = p.apply(pri_return, periods=21 * months)
            out = out.apply(StandardScaler, axis=1)
            out = out.apply(Winsorize, lower=-3, upper=3)
            return out

        px = self.universe.tr_last
        factor = (momentum(px, 6) + momentum(px, 12)) / 2

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


class PxMomRev1(Factor):
    months = 1
    def fit(self) -> pd.DataFrame:
        tr_last = self.universe.tr_last
        return tr_last.shift(self.months * 21) / tr_last


class PxMom1(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        return self.universe.tr_last.pct_change(21 * self.months)


class PxMom2(PxMom1):
    months = 2


class PxMom3(PxMom1):
    months = 3


class PxMom4(PxMom1):
    months = 4


class PxMom5(PxMom1):
    months = 5


class PxMom6(PxMom1):
    months = 6


class PxMom7(PxMom1):
    months = 7


class PxMom8(PxMom1):
    months = 8


class PxMom9(PxMom1):
    months = 9


class PxMom10(PxMom1):
    months = 10


class PxMom11(PxMom1):
    months = 11


class PxMom12(PxMom1):
    months = 12


class PxMom18(PxMom1):
    months = 18


class PxMom24(PxMom1):
    months = 24


class PxMom36(PxMom1):
    months = 36


class PxMomAbs1M(Factor):
    months = 1

    def fit(self) -> pd.DataFrame:
        return self.universe.tr_last.pct_change(21 * self.months).abs()


class PxMomAbs8(PxMomAbs1M):
    months = 8
