from .norm import *
from .scaler import *
from .cov import *

import numpy as np
import pandas as pd


def VAR(data: pd.Series, ddof: int = 1) -> float:
    return float(data.var(ddof=ddof))


def STDEV(data: pd.Series, ddof: int = 1) -> float:
    return np.sqrt(VAR(data=data, ddof=ddof))


def ENTP(data: pd.Series, window: int = 10, base=2.0) -> pd.Series:
    """Entropy (ENTP)

    Introduced by Claude Shannon in 1948, entropy measures the unpredictability
    of the data, or equivalently, of its average information. A die has higher
    entropy (p=1/6) versus a coin (p=1/2).

    Sources:
        https://en.wikipedia.org/wiki/Entropy_(information_theory)
    """
    p = data / data.rolling(window=window).sum()
    entropy = (-p * np.log(p) / np.log(base)).rolling(window=window).sum()
    return entropy


def CV(data: pd.Series, window: int = 10) -> pd.Series:
    roll = data.rolling(window=window)
    return roll.std() / roll.mean()


def Winsorize(data: pd.Series, lower: float = -3.0, upper: float = 3.0) -> pd.Series:
    return data.clip(lower=lower, upper=upper)
