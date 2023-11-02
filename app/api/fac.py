from typing import Callable, Dict
import pandas as pd
from universe import Universe
from app import core


def PxMom1M(universe: Universe) -> pd.DataFrame:
    return core.pri_return(data=universe.get_prices(), periods=21)


class Factor:
    factors = {"PxMom1M": PxMom1M}

    @classmethod
    def load_all(cls, universe: Universe) -> Dict[str, "Factor"]:
        return {key: cls(universe, value) for key, value in cls.factors.items()}




    def __init__(
        self, universe: Universe, func: Callable[[Universe], pd.DataFrame]
    ) -> None:
        self.cache = {}
        self.func = func
