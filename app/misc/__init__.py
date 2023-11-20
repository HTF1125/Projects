import pandas as pd


def datetimeindex_to_int(idx: pd.DatetimeIndex) -> pd.Index:
    from datetime import date
    return pd.to_timedelta(idx - pd.Timestamp(date(1900, 1, 1))).days + 1
