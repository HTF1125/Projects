"""ROBERT"""
import logging
from typing import List
from typing import Dict
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import declarative_base
from app.database.common import Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class TbBase(Base):
    __abstract__ = True

    @classmethod
    def get(cls, **kwargs) -> List[Dict]:
        query = select(cls)
        if kwargs:
            query = query.filter_by(**kwargs)
        with Session() as session:
            return [rec.dict() for rec in session.execute(query).scalars()]

    @classmethod
    def delete(cls, **kwargs):
        query = delete(cls)
        if kwargs:
            query = query.filter_by(**kwargs)
        with Session() as session:
            session.execute(query)
            session.commit()

    @classmethod
    def insert(cls, records):
        with Session() as session:
            try:
                session.bulk_insert_mappings(cls, records)
                session.commit()
            except Exception:
                session.rollback()

    @classmethod
    def update(cls, records):
        with Session() as session:
            try:
                session.bulk_update_mappings(cls, records)
                session.commit()
            except Exception:
                session.rollback()

    @classmethod
    def add(cls, **kwargs):
        with Session() as session:
            try:
                session.add(cls(**kwargs))
                session.commit()
            except Exception:
                session.rollback()


    @classmethod
    def has(cls, **kwargs) -> bool:
        stmt = select(cls).filter_by(**kwargs)
        with Session() as session:
            if session.query(stmt.exists()).scalar():
                return True
            return False