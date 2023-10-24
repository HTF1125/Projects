"""ROBERT"""
from typing import List
from typing import Dict
from functools import lru_cache
import pandas as pd
from app.database.common import Engine
from app.database.common import Session
from app.database.models import TbMeta
from app.database.models import TbPxDaily
from app.database.models import TbGlossary


@lru_cache()
def get_prices(tickers: str) -> pd.DataFrame:
    """query prices form database"""
    with Session() as session:
        query = session.query(
            TbMeta.code.label("Ticker"),
            TbPxDaily.date.label("Date"),
            TbPxDaily.px_adj_close.label("AdjClose"),
        ).join(TbPxDaily, TbMeta.id == TbPxDaily.meta_id)
        if tickers:
            query = query.filter(TbMeta.code.in_(tickers.replace(",", " ").split()))
        return pd.read_sql(
            sql=query.statement, con=session.connection(), parse_dates=["Date"]
        ).pivot(index="Date", columns="Ticker", values="AdjClose")


@lru_cache()
def get_volumes(tickers: str) -> pd.DataFrame:
    """query prices form database"""
    with Session() as session:
        query = session.query(
            TbMeta.code.label("Ticker"),
            TbPxDaily.date.label("Date"),
            TbPxDaily.px_volume.label("Volume"),
        ).join(TbPxDaily, TbMeta.id == TbPxDaily.meta_id)
        if tickers:
            query = query.filter(TbMeta.code.in_(tickers.replace(",", " ").split()))

        return pd.read_sql(
            sql=query.statement, con=session.connection(), parse_dates=["Date"]
        ).pivot(index="Date", columns="Ticker", values="Volume")


def get_glossaries() -> List[Dict]:
    """this is a pass through function"""
    return TbGlossary.get()


def read_sql(sql: str, **kwargs) -> pd.DataFrame:
    """this is a pass through function"""
    return pd.read_sql(sql=sql, con=Engine(), **kwargs)
