from typing import Union
import pandas as pd
from .metrics import log_return
import pandas_ta


####################################################################################################
# Uncategorized
####################################################################################################
def SMA(
    close: pd.Series,
    periods: int = 5,
) -> pd.Series:
    return close.rolling(periods).mean()


def STDEV(
    close: pd.Series,
    periods: int = 5,
) -> pd.Series:
    return log_return(close.rolling(periods).mean())


def EMA(close: pd.Series, window: int = 5) -> pd.Series:
    return close.ewm(span=window).mean()


def MACD(
    close: pd.Series,
    window1: int = 12,
    window2: int = 26,
    window3: int = 9,
) -> pd.Series:
    ema1 = EMA(close, window=window1)
    ema2 = EMA(close, window=window2)
    macd = ema1 - ema2
    macd_s = EMA(close=macd, window=window3)
    return macd_s - macd


def RMA(close: pd.Series, periods: int = 10) -> pd.Series:
    return close.ewm(alpha=(1.0 / periods)).mean()


def RSI(
    close: pd.Series,
    periods: int = 26,
) -> pd.Series:
    pos = close.diff()
    neg = pos.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0
    pos_rma = RMA(close=pos, periods=periods)
    neg_rma = RMA(close=neg, periods=periods)
    return pos_rma / (pos_rma + neg_rma.abs())


def BBand_(close: pd.Series, window: int = 5) -> pd.DataFrame:
    return None


def BBand(
    close: pd.Series,
    periods: int = 20,
) -> pd.Series:
    sma = SMA(close=close, periods=periods)
    vol = STDEV(close=close, periods=periods)
    top = sma + 2 * vol
    bot = sma - 2 * vol
    return (bot - close) / (top - close)
