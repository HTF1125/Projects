"""ROBERT"""
# import pandas as pd
# from app.db.client.base import get_prices


# def get_oecd_us_lei() -> pd.Series:
#     """this is a pass through function"""
#     return get_prices(tickers="^OECDUSCLI").squeeze()


# def get_vix() -> pd.Series:
#     """this is a pass through function"""
#     return get_prices(tickers="^VIX").squeeze()


# def get_sp500() -> pd.Series:
#     """this is a pass through function"""
#     return get_prices(tickers="^GSPC").squeeze()


# def get_dollar_index() -> pd.Series:
#     """this is a pass through function"""
#     return get_prices(tickers="^DXY").squeeze()


# def get_yields() -> pd.DataFrame:
#     """this is a pass through function"""
#     tickers = {
#         "DGS1MO": "1M",
#         "DGS3MO": "3M",
#         "DGS6MO": "6M",
#         "DGS1": "1Y",
#         "DGS2": "2Y",
#         "DGS3": "3Y",
#         "DGS5": "5Y",
#         "DGS10": "10Y",
#         "DGS20": "20Y",
#         "DGS30": "30Y",
#     }

#     data = get_prices(tickers=", ".join(list(tickers.keys())))
#     data = data.rename(columns=tickers)
#     data = data.filter(items=list(tickers.values()))
#     return data
