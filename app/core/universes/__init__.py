"""ROBERT"""
from .base import Universe
from .extension import UsSectors, GlobalAllo

__all__ = ("UsSectors", "GlobalAllo")


def instance(name: str) -> Universe:
    import sys

    inst = getattr(sys.modules[__name__], "name", None)
    if isinstance(inst, Universe):
        return inst
    raise ValueError("unable to instance")
