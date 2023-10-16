"""ROBERT"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from .engine import Engine


@contextmanager
def Session():
    """Provide a transactional scope around a series of operations."""
    session = scoped_session(sessionmaker(bind=Engine()))()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
