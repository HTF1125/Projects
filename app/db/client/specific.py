"""ROBERT"""
import pandas as pd
from .base import get_data


def get_oecd_us_lei() -> pd.Series:
    """this is a pass through function"""
    data = get_data(tickers="^OECDUSCLI", factors="PX_LAST")
    return data.squeeze()


def get_vix() -> pd.Series:
    """this is a pass through function"""
    data = get_data(tickers="^VIX", factors="PX_LAST")
    return data.squeeze()


def get_dollar_index() -> pd.Series:
    """this is a pass through function"""
    data = get_data(tickers="^DXY", factors="PX_LAST")
    return data.squeeze()


def get_sp500() -> pd.Series:
    """this is a pass through function"""
    data = get_data(tickers="^GSPC", factors="PX_LAST")
    return data.squeeze()


def get_yields() -> pd.DataFrame:
    """this is a pass through function"""
    tickers = {
        "DGS1MO": "1M",
        "DGS3MO": "3M",
        "DGS6MO": "6M",
        "DGS1": "1Y",
        "DGS2": "2Y",
        "DGS3": "3Y",
        "DGS5": "5Y",
        "DGS10": "10Y",
        "DGS20": "20Y",
        "DGS30": "30Y",
    }
    data = get_data(tickers=list(tickers.keys()), factors="PX_LAST")
    data = data.rename(columns=tickers)
    data = data.filter(items=list(tickers.values()))
    return data
