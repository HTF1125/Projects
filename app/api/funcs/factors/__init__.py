"""ROBERT"""


__all__ = [
    # "PxMo1M",
    # "PxMo2M",
    # "PxMo3M",
    # "PxMo4M",
    # "PxMo5M",
    # "PxMo6M",
    # "PxMo7M",
    # "PxMo8M",
    # "PxMo9M",
    # "PxMo10M",
    # "PxMo11M",
    # "PxMo12M",
    # "PxMo18M",
    # "PxMo24M",
    # "PxMo36M",
    # "PxMo3M2M",
    # "PxMo6M2M",
    # "PxMo9M2M",
    # "PxMo12M2M",
    # "PxMo18M2M",
    # "PxMo24M2M",
    # "PxMo36M2M",
    "Momentum",
    "MinVolatility",
    "Vcv1M",
    "Vcv3M",
    "Vcv6M",
    # "PxVol1M",
    # "PxVol3M",
    # "UsCli3Y",
    "UsCli5Y",
    # "UsCli10Y",
    "Vix3Y",
    # "Vix5Y",
    # "Vix10Y",
]


import pandas as pd
from ...universes import Universe
from ..regime import UsLei, VolState, AbsorptionRatio
from .... import core


def Momentum(universe: Universe) -> pd.DataFrame:
    px = universe.tr_last
    mom6 = (
        px.apply(core.MO, window=21 * 6)
        .apply(core.StandardScaler, axis=1)
        .apply(core.Winsorize, lower=-3, upper=3, axis=1)
    )
    mom12 = (
        px.apply(core.MO, window=21 * 12)
        .apply(core.StandardScaler, axis=1)
        .apply(core.Winsorize, lower=-3, upper=3, axis=1)
    )
    factor = (mom6 + mom12) / 2

    def to_score(x) -> float:
        if x > 0:
            return 1 + x
        elif x < 0:
            return (1 - x) ** (-1)
        else:
            return 0

    return factor.applymap(to_score)


def MinVolatility(universe: Universe) -> pd.DataFrame:
    return universe.tr_last.apply(core.log_return).apply(core.STDEV, window=21 * 12)


# def PxMo1M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 1)


# def PxMo2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 2)


# def PxMo3M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 3)


# def PxMo4M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 4)


# def PxMo5M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 5)


# def PxMo6M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 6)


# def PxMo7M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 7)


# def PxMo8M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 8)


# def PxMo9M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 9)


# def PxMo10M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 10)


# def PxMo11M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 11)


# def PxMo12M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 12)


# def PxMo18M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 13)


# def PxMo24M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 24)


# def PxMo36M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 36)


# def PxMo3M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 3) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo6M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 6) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo9M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 9) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo12M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 12) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo18M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 18) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo24M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 24) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


# def PxMo36M2M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.MO, window=21 * 36) - universe.tr_last.apply(
#         core.MO, window=21 * 2
#     )


def Vcv1M(universe: Universe) -> pd.DataFrame:
    return -universe.px_volume.apply(core.CV, window=21 * 1)


def Vcv3M(universe: Universe) -> pd.DataFrame:
    return -universe.px_volume.apply(core.CV, window=21 * 3)


def Vcv6M(universe: Universe) -> pd.DataFrame:
    return -universe.px_volume.apply(core.CV, window=21 * 6)


# def PxVol1M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.log_return).apply(core.STDEV, window=21 * 1)


# def PxVol3M(universe: Universe) -> pd.DataFrame:
#     return universe.tr_last.apply(core.log_return).apply(core.STDEV, window=21 * 3)


def UsCli3Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 3 // 2))
    final.index = states.index
    return final


def UsCli5Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 5 // 2))
    final.index = states.index
    return final


def UsCli10Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 10 // 2))
    final.index = states.index
    return final


def Vix3Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 3 // 2))
    final.index = states.index
    return final


def Vix5Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 5 // 2))
    final.index = states.index
    return final


def Vix10Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.tr_last.apply(core.pri_return)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 10 // 2))
    final.index = states.index
    return final
