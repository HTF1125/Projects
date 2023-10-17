














from typing import Dict, Any, Optional





class Universe:
    __abstr__ = True
    __cache__ = {}

    def __new__(cls, *args, **kwargs):
        instance = cls.__cache__.get(cls.__name__)
        if isinstance(instance, cls):
            return instance
        instance = super().__new__(cls)
        cls.__cache__.update({cls.__name__: instance})
        instance.__cache__ = {}
        return instance


    def __init__(
        self,
        tickers: Optional[Dict[str, Any]] = None,
        factors: Optional[Dict[str, Any]] = None,
    ) -> None:

        self.tickers = tickers
        self.factors = factors





