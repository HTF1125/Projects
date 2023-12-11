"""ROBERT"""
import os
import logging
import pandas as pd
from app.db.models import Base, TbMeta, TbGlossary
from ..common import engine


logger = logging.getLogger(__name__)


def get_xlsx(sheet_name: str) -> pd.DataFrame:
    dirname = os.path.dirname(os.path.abspath(__file__))
    db_xlsx = os.path.join(dirname, "db.xlsx")
    return pd.read_excel(io=db_xlsx, sheet_name=sheet_name)


def drop():
    Base.metadata.drop_all(engine)


def create() -> None:
    logging.info("Executing Database SQL.")
    Base.metadata.create_all(engine)
    try:
        TbMeta.insert(get_xlsx("tb_meta").to_dict("records"))
        logger.info(f"Insert `TbMeta` Sucessful.")
    except:
        logger.warning(f"Insert `TbMeta` Failed.")
    try:
        TbGlossary.insert(get_xlsx("tb_glossary").to_dict("records"))
        logger.info(f"Insert `TbGlossary` Sucessful.")
    except:
        logger.warning(f"Insert `TbGlossary` Failed.")
