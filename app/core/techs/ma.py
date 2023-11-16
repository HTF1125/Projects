import numpy as np
import pandas as pd


def SMA(close: pd.Series, window: int = 5) -> pd.Series:
    data = close.rolling(window=window).mean()
    data.name = f"SMA_{window}"
    return data


def EMA(close: pd.Series, window: int = 10) -> pd.Series:
    data = close.ewm.(span=window).mean()
    data.name = f"EMA_{window}"
    return data

def RMA(close: pd.Series, window: int = 10) -> pd.Series:
    alpha = 1.0 / window
    data = close.ewm(alpha=alpha).mean()
    data.name = f"RMA_{window}"
    return data


def ALMA(
    close: pd.Series,
    window: int = 10,
    sigma: float = 6.0,
    dist_offset: float = 0.85,
) -> pd.Series:
    """Arnaud Legoux Moving Average (ALMA)

    The ALMA moving average uses the curve of the Normal (Gauss) distribution, which
    can be shifted from 0 to 1. This allows regulating the smoothness and high
    sensitivity of the indicator. Sigma is another parameter that is responsible for
    the shape of the curve coefficients. This moving average reduces lag of the data
    in conjunction with smoothing to reduce noise.

    Implemented for Pandas TA by rengel8 based on the source provided below.

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

    Calculation:
        refer to provided source

    Args:
        close (pd.Series): Series of 'close's
        window (int): It's period, window size. Default: 10
        sigma (float): Smoothing value. Default 6.0
        distribution_offset (float): Value to offset the distribution min 0
            (smoother), max 1 (more responsive). Default 0.85

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Pre-Calculations
    m = dist_offset * (window - 1)
    s = window / sigma
    wtd = list(range(window))
    for i in range(0, window):
        wtd[i] = np.exp(-1 * ((i - m) * (i - m)) / (2 * s * s))

    # Calculate Result
    result = [np.nan for _ in range(0, window - 1)] + [0]
    for i in range(window, close.size):
        window_sum = 0
        cum_sum = 0
        for j in range(0, window):
            window_sum = window_sum + wtd[j] * close.iloc[i - j]
            cum_sum = cum_sum + wtd[j]

        almean = window_sum / cum_sum
        result.append(np.nan) if i == window else result.append(almean)

    alma = pd.Series(data=result, index=close.index, name=f"ALMA_{window}")
    return alma

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


def RSI(
    close: pd.Series,
    window: int = 26,
) -> pd.Series:
    pos = close.diff()
    neg = pos.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0
    pos_rma = RMA(close=pos, window=window)
    neg_rma = RMA(close=neg, window=window)
    return pos_rma / (pos_rma + neg_rma.abs())