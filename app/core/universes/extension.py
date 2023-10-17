from .base import Universe


class UsSectors(Universe):
    tickers = {
        "XLC": "XLC",
        "XLY": "XLY",
        "XLP": "XLP",
        "XLE": "XLE",
        "XLF": "XLF",
        "XLV": "XLV",
        "XLI": "XLI",
        "XLB": "XLB",
        "XLK": "XLK",
        "XLU": "XLU",
        "XLRE": "XLRE",
    }


class GlobalAllo(Universe):
    tickers = {
        "SPY": "SPY",
        "AGG": "AGG",
        "TLT": "TLT",
        "GSG": "GSG",
        "TIP": "TIP",
        "IVV": "IVV",
        "GLD": "GLD",
    }
