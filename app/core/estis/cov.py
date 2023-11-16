

from typing import Union
import numpy as np
import pandas as pd


def empirical_cov(
    x: Union[np.ndarray, pd.Series],
    y: Union[np.ndarray, pd.Series],
) -> float:
    assert len(x) == len(y), "must be the same length"
    n = len(x)
    x_mean = x.mean()
    y_mean = y.mean()
    cov = ((x - x_mean) * (y - y_mean)).sum() / (n - 1)
    return cov
