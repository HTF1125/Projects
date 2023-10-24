"""ROBERT"""
import socket
import warnings
from sqlalchemy import engine
from app.database.common.config import Config

local_engine = engine.create_engine(url=Config.LOCAL_URL, echo=True)
if Config.PGSQL_URL is not None:
    pgsql_engine = engine.create_engine(url=Config.PGSQL_URL, echo=True)
else:
    pgsql_engine = None


def check_internet_connection() -> bool:
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


def Engine() -> engine.Engine:
    if Config.ENV == "LOCAL":
        return local_engine
    if Config.ENV == "AUTO":
        if pgsql_engine is None:
            # warnings.warn("PGSQL Engine not accessable. using local engine.")
            return local_engine
        if not check_internet_connection():
            # warnings.warn("internet connection non-existant, using local engine.")
            return local_engine
        return pgsql_engine
    return local_engine
