import logging
import pandas as pd
import yfinance as yf
import pandas_datareader as pdr

logger = logging.getLogger(__name__)


def get_yahoo_data(ticker: str) -> pd.DataFrame:
    rename = {
        "Open": "PX_OPEN",
        "High": "PX_HIGH",
        "Low": "PX_LOW",
        "Close": "PX_LAST",
        "Volume": "PX_VOLUME",
        "Dividends": "DIVIDENDS",
        "Stock Splits": "SPLITS",
        "Capital Gains": "CAPITAL_GAINS",
        "Adj Close": "TR_LAST",
    }

    data = yf.download(tickers=ticker, actions=True, progress=False).dropna()
    data = data.stack().reset_index()
    data.columns = ["date", "feat", "data"]
    data["feat"] = data["feat"].map(rename)
    data = data[data["data"] != 0]
    return data


def get_fred_data(ticker: str) -> pd.DataFrame:
    data = pdr.DataReader(
        name=ticker,
        data_source="fred",
        start="1900-1-1",
        end=pd.Timestamp("now"),
    ).dropna()
    data = data.reset_index()
    data.columns = ["date", "data"]
    data["feat"] = "PX_LAST"
    return data
