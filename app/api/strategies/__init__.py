from typing import Type
from ..universes import Universe
from ..signals import Signal
from ..factors import Factor


class Strategy:
    def __init__(
        self,
        universe: Universe,
        frequency: int = 1,
        min_assets: int = 2,
        min_periods: int = 21,
    ) -> None:
        self.universe = universe
        self.frequency = frequency
        self.min_assets = min_assets
        self.min_periods = min_periods
        self.signals = []
        self.factors = []

    def add_signal(self, signal: Type[Signal]) -> "Strategy":
        self.signals.append(signal)
        return self

    def add_factor(self, factor: Type[Factor]) -> "Strategy":
        self.factors.append(factor)
        return self

    def backtest(self) -> "Strategy":
        return self
