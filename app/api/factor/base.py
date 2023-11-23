



import pandas as pd
from ..universe import Universe
from ..regime import UsLei, VolState, AbsorptionRatio
from ... import core


def PxMo1M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 1)


def PxMo2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 2)


def PxMo3M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 3)


def PxMo4M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 4)


def PxMo5M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 5)


def PxMo6M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 6)


def PxMo7M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 7)


def PxMo8M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 8)


def PxMo9M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 9)


def PxMo10M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 10)


def PxMo11M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 11)


def PxMo12M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 12)


def PxMo18M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 13)


def PxMo24M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 24)


def PxMo36M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 36)


def PxMo3M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 3) - px_last.apply(core.MO, window=21 * 2)


def PxMo6M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 6) - px_last.apply(core.MO, window=21 * 2)


def PxMo9M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 9) - px_last.apply(core.MO, window=21 * 2)


def PxMo12M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 10) - px_last.apply(
        core.MO, window=21 * 2
    )


def PxMo18M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 10) - px_last.apply(
        core.MO, window=21 * 2
    )


def PxMo24M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 24) - px_last.apply(
        core.MO, window=21 * 2
    )


def PxMo36M2M(universe: Universe) -> pd.DataFrame:
    px_last = universe.get_prices()
    return px_last.apply(core.MO, window=21 * 36) - px_last.apply(
        core.MO, window=21 * 2
    )


def Vcv1M(universe: Universe) -> pd.DataFrame:
    px_volume = universe.get_volumes()
    return -px_volume.apply(core.CV, window=21 * 1)


def Vcv3M(universe: Universe) -> pd.DataFrame:
    px_volume = universe.get_volumes()
    return -px_volume.apply(core.CV, window=21 * 3)


def Vcv6M(universe: Universe) -> pd.DataFrame:
    px_volume = universe.get_volumes()
    return -px_volume.apply(core.CV, window=21 * 6)


def PxVol1M(universe: Universe) -> pd.DataFrame:
    return universe.get_prices().apply(core.log_return).apply(core.STDEV, window=21 * 1)


def PxVol3M(universe: Universe) -> pd.DataFrame:
    return universe.get_prices().apply(core.log_return).apply(core.STDEV, window=21 * 3)


def UsCli3Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 3 // 2))
    final.index = states.index
    return final


def UsCli5Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 5 // 2))
    final.index = states.index
    return final


def UsCli10Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = UsLei().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 10 // 2))
    final.index = states.index
    return final


def Vix3Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 3 // 2))
    final.index = states.index
    return final


def Vix5Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 5 // 2))
    final.index = states.index
    return final


def Vix10Y(universe: Universe) -> pd.DataFrame:
    pri_return = universe.get_prices().apply(core.pri_return, forward=True)
    states = VolState().fit().states.reindex(pri_return.index).ffill()
    grouped = pri_return.set_index(states, append=True).groupby(by=[states.name])
    final = grouped.transform(core.EMA, window=(252 * 10 // 2))
    final.index = states.index
    return final
