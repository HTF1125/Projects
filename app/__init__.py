"""ROBERT"""
from . import core
from . import db
from . import web
from .api import factor
from .api import Universe
def init_logger():
    import logging

    logger = logging.getLogger("app")
    logging.captureWarnings(capture=True)
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    formatter = logging.Formatter(fmt)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    streamhandler.setLevel(logging.DEBUG)
    logger.addHandler(streamhandler)
    logger.setLevel(logging.DEBUG)


init_logger()
