"""ROBERT"""
from typing import Union
import numpy as np
import pandas as pd


def pri_return(
    px_last: pd.Series,
    periods: int = 1,
    forward: bool = False,
    demeaned: bool = False,
) -> pd.Series:
    out = px_last / px_last.shift(1) - 1
    if forward:
        return out.shift(periods=-periods).iloc[:-periods]
    return out.iloc[periods:]


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


def information_coefficient(
    forward_returns: pd.DataFrame,
    factor_data: pd.DataFrame,
) -> pd.Series:
    """
    Calculate the information coefficient between forward returns and factor data.

    Args:
        forward_returns (pd.DataFrame): DataFrame containing forward returns data.
        factor_data (pd.DataFrame): DataFrame containing factor data.

    Returns:
        pd.Series: Series containing information coefficients calculated for each date.
    """
    # Combine the data
    from scipy.stats import spearmanr

    combined_data = pd.concat([forward_returns.stack(), factor_data.stack()], axis=1)
    combined_data = combined_data.dropna().reset_index()
    combined_data.columns = ["Date", "Ticker", "Factor", "Return"]

    # Calculate information coefficient for each date
    info_coefficient = combined_data.groupby("Date").apply(
        lambda x: spearmanr(a=x["Factor"], b=x["Return"])[0]
    )
    info_coefficient.name = "InformationCoefficient"

    return info_coefficient


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
    return np.mean(np.partition(returns, cutoff_index)[:cutoff_index + 1])

