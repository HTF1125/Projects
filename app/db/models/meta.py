"""ROBERT"""
from typing import Dict
import pandas as pd
from sqlalchemy import Column, Integer, VARCHAR, Text, Float, Date, String
from sqlalchemy import ForeignKey
from ..common import Session, Engine
from .base import TbBase


class TbMeta(TbBase):
    __tablename__ = "tb_meta"
    id = Column(Integer, autoincrement=True, primary_key=True)
    ticker = Column(VARCHAR(30))
    exchange = Column(VARCHAR(30), nullable=True)
    market = Column(VARCHAR(30))
    name = Column(VARCHAR(255), nullable=False)
    source = Column(VARCHAR(30), nullable=True)
    yah = Column(VARCHAR(30), nullable=True)
    fre = Column(VARCHAR(30), nullable=True)
    bbg = Column(VARCHAR(30), nullable=True)


class TbData(TbBase):
    __tablename__ = "tb_data"
    meta_id = Column(
        ForeignKey(f"{TbMeta.__tablename__}.id"),
        primary_key=True,
    )
    feat = Column(String(30), primary_key=True)
    date = Column(Date, primary_key=True)
    data = Column(Float, nullable=False)
