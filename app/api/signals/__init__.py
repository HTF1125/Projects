from .base import *
import sys
import inspect
from typing import List


def all() -> List[Signal]:
    subclasses = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Signal) and obj is not Signal:
            subclasses.append(obj)
    return subclasses


__all__ = (
    "OecdUsCli",
    "VixMomentum",
    "SilverGoldRatio",
    "CapacityUtilization",
    "AudCadMom",
)