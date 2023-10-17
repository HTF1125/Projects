"""ROBERT"""
"""ROBERT"""
from typing import Type, Union, Dict
import pandas as pd
from app import database
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
        cls.cache.update({cls.__name__: instance})
        instance.cache = {}
        return instance

    @classmethod
    def instance(cls) -> "Universe":
        return cls(
            tickers=getattr(cls, "tickers", {}),
            factors=getattr(cls, "factors", {}),
        )

    def __init__(
        self,
        tickers: Dict = {},
        factors: Dict = {},
    ) -> None:
        self.tickers = tickers
        self.factors = factors

    def get_prices(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        if "prices" not in self.cache:
            self.cache["prices"] = database.get_prices(tickers=list(self.tickers.keys()))
        return self.cache["prices"]

    def get_volumes(self) -> pd.DataFrame:
        """
        Retrieve and cache historical prices of the specified tickers.

        Returns:
            pd.DataFrame: A DataFrame containing historical prices for the tickers.
        """
        if "prices" not in self.cache:
            self.cache["prices"] = database.get_volumes(tickers=list(self.tickers.keys()))
        return self.cache["prices"]
    def add_factor(self, *items: Union[str, Type["factors.Factor"]]) -> "Universe":
        for item in items:
            key = item if isinstance(item, str) else item.__name__
            if key not in self.factors:
                item = getattr(factors, item) if isinstance(item, str) else item
                self.factors.update({item.__name__: item(self).fit()})
        return self

    def add_ticker(self, *items: str) -> "Universe":
        for item in items:
            key = item if isinstance(item, str) else item.__name__
            if key not in self.tickers:
                self.tickers.update({key: key})
        return self
