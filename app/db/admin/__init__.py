"""ROBERT"""
import os
import logging
import warnings
from pandas import Timestamp
import pandas as pd
import yfinance as yf
import pandas_datareader as pdr
from app.db import Session, Engine, Config
from app.db.models import Base, TbMeta, TbPxDaily, TbGlossary
from app.db.common.engine import local_engine, pgsql_engine

logger = logging.getLogger(__file__)


def get_data(sheet_name: str) -> pd.DataFrame:
    dirname = os.path.dirname(os.path.abspath(__file__))
    db_xlsx = os.path.join(dirname, "db.xlsx")
    return pd.read_excel(io=db_xlsx, sheet_name=sheet_name)


def create_all(run_update: bool = True):
    drop_all()
    Base.metadata.create_all(Engine())
    if not Config.is_local():
        TbMeta.insert(get_data("tb_meta").to_dict("records"))
        TbGlossary.insert(get_data("tb_glossary").to_dict("records"))
    if run_update:
        update_px()


def drop_all():
    Base.metadata.drop_all(Engine())


def add_meta():
    if Config.ENV != "LOCAL":
        for rec in get_data("tb_meta").to_dict("records"):
            try:
                TbMeta.add(**rec)
            except:
                continue


def update_px():
    if Config.is_local():
        warnings.warn("Unable to run `update_px` with local database.")
        return

    with Session() as session:
        for meta in session.query(TbMeta).order_by(TbMeta.source).all():
            try:
                if meta.source == "YAHOO":
                    data = yf.download(
                        tickers=meta.source_code,
                        actions=True,
                        progress=False,
                    ).reset_index()
                    rename = {
                        "Date": "date",
                        "Open": "px_open",
                        "High": "px_high",
                        "Low": "px_low",
                        "Close": "px_close",
                        "Adj Close": "px_adj_close",
                        "Volume": "px_volume",
                        "Dividends": "px_dvds",
                        "Stock Splits": "px_splits",
                    }
                    data = data.rename(columns=rename)
                elif meta.source == "FRED":
                    data = pdr.DataReader(
                        name=meta.source_code,
                        data_source="fred",
                        start="1900-1-1",
                        end=Timestamp("now"),
                    )
                    if meta.frequency not in ["D", "W"]:
                        data = data.resample(meta.frequency).last().ffill()
                    data = data.reset_index()
                    data.columns = ["date", "px_adj_close"]
                else:
                    continue
                if isinstance(data, pd.DataFrame):
                    data["meta_id"] = meta.id
                    data = data.dropna()
                    session.query(TbPxDaily).where(
                        TbPxDaily.meta_id == meta.id
                    ).delete()
                    session.flush()
                    session.bulk_insert_mappings(TbPxDaily, data.to_dict("records"))
                    session.commit()
            except Exception as exc:
                logger.exception(exc)


def download_db() -> None:
    if pgsql_engine is None:
        return
    table_name = "balance_sheet"
    df = pd.read_sql(sql=f"SELECT * FROM {table_name}", con=pgsql_engine)
    df.to_sql(name=table_name, con=local_engine, if_exists="replace", index=False)

    tbs = [TbMeta, TbGlossary, TbPxDaily]
    Config.is_local()
    create_all(False)
    for tb in tbs:
        Config.use_auto()
        df = tb.get()
        Config.use_local()
        tb.insert(df)
