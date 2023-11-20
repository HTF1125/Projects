from .universe import Universe

import pandas as pd


class Portflio:
    def __init__(
        self,
        assets: pd.Index,
        expected_returns: pd.Series,
        covariance_matrix: pd.DataFrame,
    ) -> None:
        self.assets = assets
        self.expected_returns = expected_returns
        self.covariance_matrix = covariance_matrix

