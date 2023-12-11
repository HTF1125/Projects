<<<<<<< HEAD
from typing import Union, List, Set, Tuple
import os
=======
from functools import lru_cache
from typing import Union, List, Set, Tuple
from sqlalchemy import select
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
import pandas as pd


def get_data(
    tickers: Union[str, List[str], Set[str], Tuple[str, ...]],
    fields: Union[str, List[str], Set[str], Tuple[str, ...]] = "PX_LAST",
) -> pd.DataFrame:
    filename = os.path.join(
        os.path.dirname(__file__),
        "static",
        f"{fields}.feather",
    )

    if not os.path.exists(filename):
        raise ValueError("....")

    data = pd.read_feather(filename)

    tickers = list(
        tickers
        if isinstance(tickers, (list, set, tuple))
        else tickers.replace(",", " ").split()
    )

    return data.filter(items=tickers).dropna(how="all")


def get_universe() -> pd.DataFrame:
    filename = os.path.join(
        os.path.dirname(__file__),
        "static",
        f"db.xlsx",
    )
    if not os.path.exists(filename):
        raise ValueError("....")

    return pd.read_excel(filename, sheet_name="Universe", index_col=0)


def get_assets(universe: str = "SP500") -> List[str]:
    return get_universe().loc[universe].Assets.to_list()


def get_meta() -> pd.DataFrame:
    filename = os.path.join(
        os.path.dirname(__file__),
        "static",
        f"db.xlsx",
    )
    if not os.path.exists(filename):
        raise ValueError("....")

    return pd.read_excel(filename, sheet_name="Meta", index_col=0)


def update_meta() -> bool:
    import yfinance as yf
    import pandas_datareader as pdr

    meta = get_meta()

    meta_fred = meta[meta.source == "FRED"]

    fred_data = []
    for ticker in meta_fred.fred:
        fred_data.append(
            pdr.DataReader(
                name=ticker,
                data_source="fred",
                start="1900-1-1",
                end=pd.Timestamp("now"),
            ).dropna()
        )
<<<<<<< HEAD
    fred_data = pd.concat(fred_data, axis=1)
=======

    tickers = validate(tickers)
    factors = validate(factors)
    cols = [
        TbData.date.label("Date"),
        TbData.data.label("Data"),
        TbMeta.ticker.label("Ticker"),
    ]
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302

    meta_yahoo = meta[meta.source == "YAHOO"]
    yahoo_data = yf.download(
        tickers=list(meta_yahoo.index), actions=True, progress=True
    )

<<<<<<< HEAD
    columns = {
        "TR_LAST": "Adj Close",
        "PX_LAST": "Close",
        "PX_OPEN": "Open",
        "PX_HIGH": "High",
        "PX_LOW": "Low",
        "PX_DVDS": "Dividends",
        "PX_SPLITS": "Stock Splits",
        "PX_VOLUME": "Volume",
    }

    for new, old in columns.items():
        if new == "PX_LAST":
            data = pd.concat([yahoo_data[old], fred_data], axis=1)
        else:
            data = yahoo_data[old]
        filename = os.path.join(
            os.path.dirname(__file__),
            "static",
            f"{new}.feather",
        )
        data.to_feather(filename)

    return True
=======
    with Session() as session:
        query = session.query(*cols).join(TbMeta, TbMeta.id == TbData.meta_id)
        query = query.filter(TbMeta.ticker.in_(tickers))
        query = query.filter(TbData.factor.in_(factors))
        data = pd.read_sql(
            sql=query.statement,
            con=session.connection(),
            parse_dates=["Date"],
        )
        idxs = ["Date"]
        cols = list(set(data.columns) - set(idxs) - set(["Data"]))
        data = pd.pivot(data=data, index=idxs, columns=cols, values="Data")
        data = data.sort_index(axis=1)
    return data
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
