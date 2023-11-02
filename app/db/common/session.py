"""ROBERT"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from .engine import Engine

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
