import pandas as pd
from .ma import SMA, EMA


def AO(high: pd.Series, low: pd.Series, fast: int = 5, slow: int = 34) -> pd.Series:
    med_price = (high + low) * 0.5
    sma_fast = SMA(med_price, fast)
    sma_slow = SMA(med_price, slow)
    data = sma_fast - sma_slow
    data.name = f"AO_{fast}_{slow}"
    return data


def MO(px_last: pd.Series, window: int = 20) -> pd.Series:
    """
    The Momentum Oscillator measures the amount that a security’s price has changed over a given
    period of time. The Momentum Oscillator is the current price divided by the price of a previous
    period, and the quotient is multiplied by 100. The result is an indicator that oscillates around
    100. Values less than 100 indicate negative momentum, or decreasing price, and vice versa.

    If the Momentum Oscillator reaches extremely high or low values (relative to its historical
    values), you should assume a continuation of the current trend.

    Since the Momentum Oscillator does not have an upper and lower boundary you must visually
    inspect the history of the momentum line and draw horizontal lines along its upper and lower
    boundaries. When the momentum line reaches these levels it may indicate that the stock may be
    overbought or oversold. Note: The Momentum Oscillator is an unbound oscillator, meaning there is
    no upside or downside limits. This makes interpreting an overbought or oversold condition
    subjective. When the Momentum Oscillator is overbought the security can continue to move higher.
    When the Momentum Oscillator is oversold the security can continue lower as well. Use the
    Momentum Oscillator in conjunction with additional indicators or price analysis when attempting
    to read overbought or oversold conditions.

    If underlying prices make a new high or low that isn't confirmed by the Momentum Indicator, the
    divergence may signal a price reversal.
    """
    return (px_last / px_last.shift(window)).dropna() * 100


def APO(px_last: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
    """
    The Absolute Price Oscillator displays the difference between two exponential moving averages
    of a security's price and is expressed as an absolute value.

    - APO crossing above zero is considered bullish, while crossing below zero is bearish.
    - A positive indicator value indicates an upward trend, vise versa.


    Args:
        close (pd.Series): _description_
        fast (int, optional): _description_. Defaults to 12.
        slow (int, optional): _description_. Defaults to 26.

    Returns:
        pd.Series: _description_
    """
    sma_fast = EMA(px_last, fast)
    sma_slow = EMA(px_last, slow)
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
