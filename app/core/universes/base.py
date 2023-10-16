"""ROBERT"""
"""ROBERT"""
from typing import Optional, List, Type, Union
import numpy as np
import pandas as pd
from app import database
from app.core import stats
from app.core import factors


class Universe:
    """
    A class for managing and analyzing financial data related to a universe of assets.

    Attributes:
        tickers (List[str]): A list of asset tickers.
    """
    cache = {}

    def __new__(cls, *args, **kwargs):
        instance = cls.cache.get(cls.__name__)
        if isinstance(instance, cls):
            return instance
        instance = super().__new__(cls)
        instance.cache = {}
        cls.cache.update({cls.__name__: instance})
        return instance

    tickers = []

    def __init__(self, tickers: Optional[List[str]] = None) -> None:
        """
        Initialize a Universe object with an empty list of tickers.
        """
        self.tickers = tickers if isinstance(tickers, list) else self.tickers


    def get_prices(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        key = "PRICE"
        if key not in self.cache:
            self.cache[key] = database.get_prices(self.tickers)
        return self.cache[key]

    def get_volumes(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        key = "VOLUME"
        if key not in self.cache:
            self.cache[key] = database.get_volumes(self.tickers)
        return self.cache[key]

    def add_factor(self, *args: Union[str, Type["factors.Factor"]]) -> "Universe":
        if "factors" not in self.cache:
            self.cache["factors"] = {}
        for arg in args:
            key = arg if isinstance(arg, str) else arg.__name__
            if key not in self.cache["factors"]:
                arg = getattr(factors, arg) if isinstance(arg, str) else arg
                self.cache["factors"][key] = arg(self).fit()
        return self
