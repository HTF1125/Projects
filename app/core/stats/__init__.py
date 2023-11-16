from .norm import *
from .scaler import *
import numpy as np
import pandas as pd


def VAR(data: pd.Series, window: int = 30, ddof: int = 1) -> pd.Series:
    return data.rolling(window=window).var(ddof=ddof)


def STDEV(data: pd.Series, window: int = 30, ddof: int = 1) -> pd.Series:
    return VAR(data=data, window=window, ddof=ddof).apply(np.sqrt)


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
