from .base import Factor
from .momt import *
from .lowv import *
from .cust import *
from .mean_reversion import *


import sys
import inspect
from typing import List


def all() -> List[Factor]:
    subclasses = []
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Factor) and obj is not Factor:
            subclasses.append(obj)
    return subclasses


__all__ = [
    "PxMom1",
    "PxMom2",
    "PxMom3",
    "PxMom4",
    "PxMom5",
    "PxMom6",
    "PxMom7",
    "PxMom8",
    "PxMomAbs1M",
    "Lowv3M",
    "MeanReversion1M",
]
