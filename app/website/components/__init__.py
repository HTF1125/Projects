"""ROBERT"""
from .common import *
from .navbar import loadNavbar
from .static import loadStatic
from .strategy import *
from .select import *
import logging

def loadLogger():
    logger = logging.getLogger("website")
    if not st.session_state.get("logger"):
        logging.captureWarnings(capture=True)
        if not logger.handlers:
            fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
            formatter = logging.Formatter(fmt)
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(formatter)
            streamhandler.setLevel(logging.DEBUG)
            logger.addHandler(streamhandler)
            logger.setLevel(logging.DEBUG)
            st.session_state["logger"] = True
            logger.info("initialize streamlit webpage.")



