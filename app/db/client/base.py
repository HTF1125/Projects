from typing import Optional, Union, List
from sqlalchemy.orm import Session
import pandas as pd
from ..common import dbSession
from ..models import TbMeta, TbData

def get_data(
    tickers: Union[str, List[str]], features: Union[str, List[str]] = "PX_LAST"
) -> pd.DataFrame:
    tickers = (
        tickers
        if isinstance(tickers, (list, set, tuple))
        else tickers.replace(",", " ").split()
    )
    features = (
        tickers
        if isinstance(features, (list, set, tuple))
        else features.replace(",", " ").split()
    )
    columns = [
        TbData.date.label("Date"),
        TbData.data.label("Data"),
        TbMeta.ticker.label("Ticker"),
    ]

    if len(features) > 1:
        columns.insert(2, TbData.feat.label("Feature"))

    with dbSession() as session:
        query = session.query(*columns).join(
            TbMeta, TbMeta.id == TbData.meta_id
        )
        query = query.filter(TbMeta.ticker.in_(tickers))
        query = query.filter(TbData.feat.in_(features))
        data = pd.read_sql(
            sql=query.statement,
            con=session.connection(),
            parse_dates=["Date"],
        )
    index = ["Date"]
    columns = list(set(data.columns) - set(index) - set(["Data"]))
    data = pd.pivot(data=data, index=index, columns=columns, values="Data")
    data = data.sort_index(axis=1)
    return data
