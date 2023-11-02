"""ROBERT"""
import socket
from sqlalchemy import engine
import os


class Config:
    """Database Configuration"""

    ENV = "AUTO"
    LOCAL_URL = "sqlite:///app/database/db.db"
    PGSQL_URL = os.environ.get("POSTGRESQL_URL", None)

    @classmethod
    def use_auto(cls):
        """Set DB Environment to AUTO"""
        cls.ENV = "AUTO"

    @classmethod
    def use_local(cls):
        """Set DB Environment to LOCAL"""
        cls.ENV = "LOCAL"

    @classmethod
    def is_local(cls) -> bool:
        """Check if DB Environment is LOCAL"""
        return cls.ENV == "LOCAL"

local_engine = engine.create_engine(url=Config.LOCAL_URL, echo=False)
if Config.PGSQL_URL is not None:
    pgsql_engine = engine.create_engine(url=Config.PGSQL_URL, echo=False)
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



from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

SessionFactor = sessionmaker(bind=Engine())
ScopedSession = scoped_session(SessionFactor)

@contextmanager
def Session():
    """
    Provide a transactional scope around a series of operations.
    """
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
