import pandas as pd

from .ma import SMA


def Envelope(px_last: pd.Series, spread: float = 0.05) -> pd.DataFrame:
    sma = SMA(px_last=px_last)
    ub = sma * (1 + spread)
    lb = sma * (1 - spread)
    out = pd.concat([sma, ub, lb], axis=1)
    return out

