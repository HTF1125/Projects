from typing import Union
import pandas as pd
from .metrics import log_return

####################################################################################################
# Uncategorized
####################################################################################################
def SMA(
    data: pd.DataFrame,
    periods: int = 5,
) -> pd.DataFrame:
    return data.rolling(periods).mean()


def VOL(
    data: pd.DataFrame,
    periods: int = 5,
) -> pd.DataFrame:
    return data.rolling(periods).mean()

def EMA(data: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    return data.ewm(span=window).mean()


def MACD(
    data: pd.DataFrame,
    window1: int = 12,
    window2: int = 26,
    window3: int = 9,
) -> pd.DataFrame:
    ema1 = EMA(data, window=window1)
    ema2 = EMA(data, window=window2)
    macd = ema1 - ema2
    macd_s = EMA(data=macd, window=window3)
    return macd_s - macd


def RMA(close: pd.DataFrame, periods: int = 10) -> pd.DataFrame:
    return close.ewm(alpha=(1.0 / periods)).mean()


def RSI(
    close: pd.DataFrame,
    periods: int = 26,
) -> pd.DataFrame:
    pos = close.diff()
    neg = pos.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0
    pos_rma = RMA(close=pos, periods=periods)
    neg_rma = RMA(close=neg, periods=periods)
    return pos_rma / (pos_rma + neg_rma.abs())


def BBand(
    close: pd.DataFrame,
    periods: int = 20,
) -> pd.DataFrame:
    sma = SMA(data=close, periods=periods)
    vol = VOL(data=close, periods=periods)
    top = sma + 2 * vol
    bot = sma - 2 * vol
    return (bot - close) / (top - close)

