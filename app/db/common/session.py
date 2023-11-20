"""ROBERT"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from .engine import local_engine, pgsql_engine
from .config import Config

LocalSession = scoped_session(sessionmaker(bind=local_engine))
PgsqlSession = scoped_session(sessionmaker(bind=pgsql_engine))


@contextmanager
def dbSession():
    """
    Provide a transactional scope around a series of operations.
    """
    if Config.ENV == "LOCAL":
        session = LocalSession()
    else:
        session = PgsqlSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
