"""ROBERT"""
from typing import Dict
import pandas as pd
from sqlalchemy import Column, Integer, VARCHAR, Text, Float, Date
from sqlalchemy import ForeignKey
from app.db.common import Session
from app.db.models import TbBase


class TbMeta(TbBase):
    __tablename__ = "tb_meta"
    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(VARCHAR(30))
    name = Column(VARCHAR(255), nullable=False)
    category = Column(VARCHAR(30), nullable=True)
    instrument = Column(VARCHAR(30), nullable=True)
    frequency = Column(VARCHAR(30), nullable=True)
    source = Column(VARCHAR(30), nullable=True)
    source_code = Column(VARCHAR(30), nullable=True)
    unit = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)

    def dict(self) -> Dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "instrument": self.instrument,
            "frequency": self.frequency,
            "source": self.source,
            "source_code": self.source_code,
            "unit": self.unit,
            "remark": self.remark,
        }

    @classmethod
    def adj_close(cls, tickers) -> pd.DataFrame:
        with Session() as session:
            query = (
                session.query(
                    TbMeta.code.label("Ticker"),
                    TbPxDaily.date.label("Date"),
                    TbPxDaily.px_adj_close.label("AdjClose"),
                )
                .join(TbPxDaily, TbMeta.id == TbPxDaily.meta_id)
                .filter(TbMeta.code.in_(tickers))
            )
            return pd.read_sql_query(
                sql=query.statement,
                con=session.connection(),
                parse_dates=["Date"],
            ).pivot(index="Date", columns="Ticker", values="AdjClose")

    @classmethod
    def volume(cls, tickers) -> pd.DataFrame:
        with Session() as session:
            query = (
                session.query(
                    TbMeta.code.label("Ticker"),
                    TbPxDaily.date.label("Date"),
                    TbPxDaily.px_volume.label("Volume"),
                )
                .join(TbPxDaily, TbMeta.id == TbPxDaily.meta_id)
                .filter(TbMeta.code.in_(tickers))
            )

            return pd.read_sql_query(
                sql=query.statement,
                con=session.connection(),
                parse_dates=["Date"],
            ).pivot(index="Date", columns="Ticker", values="AdjClose")


class TbPxDaily(TbBase):
    __tablename__ = "tb_px_daily"
    meta_id = Column(ForeignKey(f"{TbMeta.__tablename__}.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    px_open = Column(Float)
    px_high = Column(Float)
    px_low = Column(Float)
    px_close = Column(Float)
    px_adj_close = Column(Float)
    px_volume = Column(Float)
    px_dvds = Column(Float)
    px_splits = Column(Float)

    def dict(self) -> Dict:
        return dict(
            date=self.date,
            meta_id=self.meta_id,
            px_open=self.px_open,
            px_high=self.px_high,
            px_low=self.px_low,
            px_close=self.px_close,
            px_adj_close=self.px_adj_close,
            px_volume=self.px_volume,
            px_dvds=self.px_dvds,
            px_splits=self.px_splits,
        )
