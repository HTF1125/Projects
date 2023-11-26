
import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


database_url = os.environ.get("POSTGRESQL_URL", "sqlite:///app/db/database.db")

engine = create_engine(database_url, echo=False, pool_size=20)

ScopedSession = scoped_session(sessionmaker(bind=engine))

logger = logging.getLogger(__name__)

@contextmanager
def Session():
    """
    Provide a transactional scope around a series of operations.
    """
    logger.debug("Creating a new session.")

    session = ScopedSession()
    try:
        yield session
        logger.debug("Committing the session.")
        session.commit()
    except Exception as e:
        logger.error(f"Error during transaction: {e}")
        session.rollback()
        raise e
    finally:
        logger.debug("Closing the session.")
        session.close()
