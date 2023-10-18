"""Robert"""

from app.api.base import Universe


class UsSectors(Universe):
    assets = {
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
    assets = {
        "SPY": "SPY",
        "AGG": "AGG",
        "TLT": "TLT",
        "GSG": "GSG",
        "TIP": "TIP",
        "IVV": "IVV",
        "GLD": "GLD",
    }
