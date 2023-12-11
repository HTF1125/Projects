import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
<<<<<<< HEAD

logger = logging.getLogger(__name__)


url = os.environ.get(
    "HEROKU_POSTGRESQL_WHITE_URL", "sqlite:///app/db/database.db"
).replace("postgres", "postgresql+psycopg2")

=======
logger = logging.getLogger(__name__)


url = os.environ.get("POSTGRESQL_URL", "sqlite:///app/db/database.db")
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302

engine = create_engine(url=url, echo=False, pool_size=20)

ScopedSession = scoped_session(sessionmaker(bind=engine))


<<<<<<< HEAD
=======

>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
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
<<<<<<< HEAD




=======
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302