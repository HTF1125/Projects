"""ROBERT"""
import os
import pandas as pd
from app.database.common import Engine
from app.database.common import Config
from app.database.models import Base, TbMeta, TbGlossary


def get_data(sheet_name: str) -> pd.DataFrame:
    dirname = os.path.dirname(os.path.abspath(__file__))
    db_xlsx = os.path.join(dirname, "db.xlsx")
    return pd.read_excel(io=db_xlsx, sheet_name=sheet_name)


def drop():
    Base.metadata.drop_all(Engine())


def create() -> None:
    drop()
    Base.metadata.create_all(Engine())
    if not Config.is_local():
        TbMeta.insert(get_data("tb_meta").to_dict("records"))
        TbGlossary.insert(get_data("tb_glossary").to_dict("records"))
