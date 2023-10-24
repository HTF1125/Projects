from .universe import Universe


class Portfolio:
    def __init__(
        self,
        universe: Universe,
    ) -> None:
        self.universe = universe
