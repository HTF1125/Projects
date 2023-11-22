
from functools import lru_cache
from typing import Union, List, Set, Tuple

import pandas as pd
from ..common import Session
from ..models import TbMeta, TbData


@lru_cache()
def get_data(
    tickers: Union[str, List[str], Set[str], Tuple[str]],
    factors: Union[str, List[str], Set[str], Tuple[str]] = "PX_LAST",
) -> pd.DataFrame:
    def validate(text: Union[str, List[str], Set[str], Tuple[str]]) -> List[str]:
        return list(
            text
            if isinstance(text, (list, set, tuple))
            else text.replace(",", " ").split()
        )
    tickers = validate(tickers)
    factors = validate(factors)
    cols = [
        TbData.date.label("Date"),
        TbData.data.label("Data"),
        TbMeta.ticker.label("Ticker"),
    ]

    if len(factors) > 1:
        # Insert factor Column at the 2nd position from the back.
        cols.insert(len(cols) - 1, TbData.factor.label("Factor"))

    with Session() as session:
        query = session.query(*cols).join(TbMeta, TbMeta.id == TbData.meta_id)
        query = query.filter(TbMeta.ticker.in_(tickers))
        query = query.filter(TbData.factor.in_(factors))
        sql = query.statement
        con = query.session.connection()
        data = pd.read_sql(sql=sql, con=con, parse_dates=["Date"])
    idxs = ["Date"]
    cols = list(set(data.columns) - set(idxs) - set(["Data"]))
    data = pd.pivot(data=data, index=idxs, columns=cols, values="Data")
    data = data.sort_index(axis=1)
    return data
