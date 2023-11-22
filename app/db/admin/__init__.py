import logging
from typing import Dict, Any
from ..models import TbMeta, TbData
from ..public import get_fred_data
from ..public import get_yahoo_data


logger = logging.getLogger(__name__)


def update_data() -> Dict[str, Any]:
    logger.debug("Start update tb_data ......")
    message = ""
    for _, meta in TbMeta.all().iterrows():
        src = str(meta.get("source")).lower()
        idx = meta.get("id")
        if not src or not idx:
            continue
        src = src[:3]
        ticker = str(meta.get(src))
        if not ticker:
            continue
        if src == "yah":
            data = get_yahoo_data(ticker)
        elif src == "fre":
            data = get_fred_data(ticker)
        else:
            msg = f"SourceNotFoundError: {meta.to_dict()}"
            logger.warning(msg)
            message += msg + "\n"
            continue
        if data.empty:
            msg = f"DataNotFoundError: {meta.to_dict()}"
            logger.warning(msg)
            message += msg + "\n"
        TbData.delete(meta_id=idx)
        data["meta_id"] = idx
        TbData.insert(data.to_dict("records"))
    return {"success": True, "message": ""}
