"""ROBERT"""
import logging
from typing import List
from typing import Dict
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import declarative_base
import pandas as pd
from ..common import Session, Engine

logger = logging.getLogger(__name__)

Base = declarative_base()


class TbBase(Base):
    __abstract__ = True

    @classmethod
    def create(cls) -> None:
        cls.__table__.create(Engine())

    @classmethod
    def drop(cls) -> None:
        cls.__table__.drop(Engine())

    @classmethod
    def get(cls, **kwargs) -> pd.DataFrame:
        query = select(cls)
        if kwargs:
            query = query.filter_by(**kwargs)
        with Session() as session:
            return pd.read_sql(sql=query, con=session.connection())

    @classmethod
    def delete(cls, **kwargs):
        query = delete(cls)
        if kwargs:
            query = query.filter_by(**kwargs)
        with Session() as session:
            session.execute(query)
            session.commit()

    @classmethod
    def insert(cls, records, chunk_size=100000000):

        if len(records) < chunk_size:
            with Session() as session:
                session.bulk_insert_mappings(cls, records)
                session.commit()
                return

        from tqdm import tqdm

        with Session() as session:
            # Calculate the number of chunks
            num_records = len(records)
            num_chunks = (num_records // chunk_size) + (
                1 if num_records % chunk_size != 0 else 0
            )

            # Create a tqdm progress bar
            progress_bar = tqdm(
                total=num_chunks, desc="Inserting Records", unit="chunk"
            )

            for i in range(num_chunks):
                # Calculate start and end indices for the current chunk
                start_index = i * chunk_size
                end_index = min((i + 1) * chunk_size, num_records)

                # Extract the current chunk
                current_chunk = records[start_index:end_index]

                # Perform bulk insert for the current chunk
                session.bulk_insert_mappings(cls, current_chunk)
                session.flush()
                # Update the progress bar
                progress_bar.update(1)

            # Close the progress bar
            progress_bar.close()

            session.commit()

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

    def save(self) -> bool:
        with Session() as session:
            session.add(self)
            session.commit()
            return True

    @classmethod
    def all(cls, **kwargs) -> pd.DataFrame:
        return pd.read_sql(sql=select(cls), con=Engine(), **kwargs)
