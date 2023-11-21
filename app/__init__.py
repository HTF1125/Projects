"""ROBERT"""


import logging

logger = logging.getLogger("app")
logging.captureWarnings(capture=True)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
streamhandler.setLevel(logging.DEBUG)
logger.addHandler(streamhandler)
logger.setLevel(logging.DEBUG)

from . import core
from . import db
from . import web
from . import api