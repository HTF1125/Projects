"""ROBERT"""
from . import core
from . import db
from . import web
<<<<<<< HEAD
from .api import Universe, factors, signals

=======
from . import api
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302

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
