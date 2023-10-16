from .base import Universe


class UsSectors(Universe):
    tickers = list("XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLK, XLU, XLRE".split(", "))


class GlobalAllo(Universe):
    tickers = list("SPY, AGG, TLT, GSG, TIP, IVV, GLD".split(", "))
