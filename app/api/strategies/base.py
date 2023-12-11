from ..universes import Universe


class Strategy:
    def __init__(
        self,
        universe: Universe,
        commission: int = 0,
    ) -> None:
        self.universe = universe
        self.commission = commission




    