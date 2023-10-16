"""ROBERT"""

import logging
from sqlalchemy.pool import Pool
from sqlalchemy.event import listens_for

logger = logging.getLogger(__name__)


@listens_for(Pool, "checkout")
def check_idle_connection(dbapi_conn, connection_record, connection_proxy):
    # This function will be called when a connection is checked out from the pool
    # Perform any checks on the connection here
    # For this example, we'll check if the connection is idle and close it if it is

    try:
        cursor = dbapi_conn.cursor()
        cursor.execute(
            "SELECT state FROM pg_stat_activity WHERE pid = pg_backend_pid();"
        )
        state = cursor.fetchone()[0]
        cursor.close()
        if state == "idle":
            logger.info("close idle connection")
            dbapi_conn.close()
            connection_proxy._pool.dispose()
    except Exception as exc:
        # logger.error(f"check idle connection failed, {exc}")
        pass
