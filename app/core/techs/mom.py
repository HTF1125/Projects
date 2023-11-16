import pandas as pd
from .ma import SMA


def AO(high: pd.Series, low: pd.Series, fast: int = 5, slow: int = 34) -> pd.Series:
    med_price = (high + low) * 0.5
    sma_fast = SMA(med_price, fast)
    sma_slow = SMA(med_price, slow)
    data = sma_fast - sma_slow
    data.name = f"AO_{fast}_{slow}"
    return data


def APO(close: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
    sma_fast = SMA(close, fast)
    sma_slow = SMA(close, slow)
    data = sma_fast - sma_slow
    data.name = f"APO_{fast}_{slow}"
    return data



def PxMom(close: pd.Series, months: int = 1) -> pd.Series:
    close = close.resample("D").last().ffill()
    base = close.copy()
    base.index = base.index + pd.DateOffset(months=months)
    return close / base - 1


def PxRevMom(close: pd.Series, mom_months: int = 6, rev_months: int = 1) -> pd.Series:
    return PxMom(close=close, months=mom_months) - PxMom(close=close, months=rev_months)
