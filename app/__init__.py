"""ROBERT"""
from . import core
from . import database
from . import web



import logging

logger = logging.getLogger("app")
logging.captureWarnings(capture=True)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
streamhandler.setLevel(logging.DEBUG)
logger.addHandler(streamhandler)
logger.setLevel(logging.DEBUG)
# logger.info("initialize streamlit webpage.")