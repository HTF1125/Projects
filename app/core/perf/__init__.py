"""ROBERT"""
from typing import Union, Optional
import numpy as np
import pandas as pd


def pri_return(
    px_last: pd.Series,
    periods: int = 1,
    forward: bool = False,
) -> pd.Series:
    out = px_last / px_last.shift(periods) - 1
    if forward:
        return out.shift(periods=-periods)
    return out


def log_return(
    px_last: pd.Series,
    periods: int = 1,
    forward: bool = False,
) -> pd.Series:
    return pri_return(px_last=px_last, periods=periods, forward=forward).apply(np.log1p)


def cum_return(
    px_last: pd.Series,
) -> pd.Series:
    px_last = px_last.dropna()  # Remove NaN values
    return px_last.iloc[-1] / px_last.iloc[0] - 1


def ann_return(
    px_last: pd.Series,
    ann_factor: Union[int, float] = 252.0,
) -> float:
    base_return = np.exp(log_return(px_last).mean()) - 1
    return base_return * ann_factor


def ann_volatility(
    px_last: pd.Series,
    ann_factor: Union[int, float] = 252.0,
) -> float:
    base_return = log_return(px_last).std()
    return base_return * ann_factor**0.5


def ann_sharpe(
    px_last: pd.Series,
    risk_free: float = 0.0,
    ann_factor: Union[int, float] = 252.0,
) -> float:
    return (
        ann_return(px_last=px_last, ann_factor=ann_factor) - risk_free
    ) / ann_volatility(px_last=px_last, ann_factor=ann_factor)


def get_absorption_ratio(data: pd.DataFrame, n_components=5, a_components: int = 3):
    from sklearn.decomposition import PCA
    from ..stat import StandardScaler

    normalized_data = data.apply(StandardScaler, axis=1)
    pca = PCA(n_components=n_components)
    pca.fit(normalized_data.values)
    explained_variance_ratio = np.sum(pca.explained_variance_ratio_[:a_components])
    return explained_variance_ratio


def MDD(px_last: pd.Series) -> pd.Series:
    return px_last / px_last.expanding().max() - 1


def VaR(px_last: pd.Series, alpha: float = 0.05) -> float:
    return np.percentile(pri_return(px_last.dropna()), 100 * alpha)


def CVaR(px_last: pd.Series, alpha: float = 0.05) -> float:
    returns = pri_return(px_last).dropna()
    cutoff_index = int((len(returns) - 1) * alpha)
    return np.mean(np.partition(returns, cutoff_index)[: cutoff_index + 1])


def turnover(weights: pd.DataFrame) -> pd.Series:
    return weights.diff().abs().sum(axis=1)


def mean_fwd_return(px_last: pd.Series, periods: int = 1) -> pd.Series:
    mean = pri_return(px_last=px_last, periods=periods, forward=True)
    mean = mean / periods
    return mean


def drawdown(px_last: pd.Series, window: Optional[int] = None) -> pd.Series:
    if window:
        return px_last / px_last.rolling(window).max() - 1
    return px_last / px_last.expanding().max() - 1


def MaxDrawDown(px_last: pd.Series, window: Optional[int] = None) -> float:
    return - drawdown(px_last=px_last, window=window).min()