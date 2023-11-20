import pandas as pd


from .. import core


def PX_MOM_1M(px_last: pd.Series) -> pd.Series:
    return core.PxMom(px_last, months=1)
