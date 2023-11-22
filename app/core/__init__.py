"""ROBERT"""
from .perf import *
from .port import *
from .stat import *
from .tech import *


def cov_to_cor(cov: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a covariance matrix to a correlation matrix.

    Parameters:
    - cov (numpy.ndarray): Covariance matrix.

    Returns:
    - numpy.ndarray: Correlation matrix.
    """
    # Extract standard deviations from the diagonal of the covariance matrix
    std = np.sqrt(np.diag(cov))
    # Compute the outer product of standard deviations to get the variance matrix
    var = np.outer(std, std)
    # Divide the covariance matrix by the variance matrix element-wise
    cor = cov.divide(var)
    return cor


def to_quantile(
    x: pd.Series,
    quantiles: int = 5,
    zero_aware: bool = False,
) -> pd.Series:
    if len(x.dropna()) < quantiles:
        return pd.Series(data=None)
    try:
        if zero_aware:
            objs = [
                to_quantile(x[x >= 0], quantiles=quantiles // 2) + quantiles // 2,
                to_quantile(x[x < 0], quantiles=quantiles // 2),
            ]
            return pd.concat(objs=objs).sort_index()
        return pd.qcut(x=x, q=quantiles, labels=False) + 1
    except ValueError:
        return pd.Series(data=None)


def sum_to_one(x):
    if isinstance(x, pd.Series):
        x = x.dropna()
    return x / sum(x)


def demeaned(x):
    if isinstance(x, pd.Series):
        x = x.dropna()
    return x - (sum(x) / len(x))


def get_sp500_ticker_list():
    # Read and print the stock tickers that make up S&P500
    tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[
        0
    ]
    return tickers
