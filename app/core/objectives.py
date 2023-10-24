"""ROBERT"""
from typing import Union
import numpy as np
import pandas as pd


def portfolio_ret(
    weights: Union[np.ndarray, pd.Series],
    returns: Union[np.ndarray, pd.Series],
) -> float:
    """Calculate the portfolio return.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    returns (np.ndarray): Array of asset returns.

    Returns:
    float: Portfolio return.
    """
    return np.dot(weights, returns)


def portfolio_var(
    weights: Union[np.ndarray, pd.Series],
    cov_matrix: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the portfolio variance.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.

    Returns:
    float: Portfolio variance.
    """
    return np.linalg.multi_dot((weights, cov_matrix, weights))


def portfolio_vol(
    weights: Union[np.ndarray, pd.Series],
    cov_matrix: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the portfolio volatility (standard deviation).

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.

    Returns:
    float: Portfolio volatility.
    """
    return portfolio_var(weights, cov_matrix) ** 0.5


def portfolio_cor(
    weights: Union[np.ndarray, pd.Series],
    cor_matrix: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the portfolio correlation.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cor_matrix (np.ndarray): Correlation matrix of asset returns.

    Returns:
    float: Portfolio correlation.
    """
    return np.linalg.multi_dot((weights, cor_matrix, weights))


def portfolio_risk_contribs(
    weights: Union[np.ndarray, pd.Series],
    cov_matrix: Union[np.ndarray, pd.DataFrame],
    percentage: bool = True,
) -> np.ndarray:
    """Calculate the risk contributions of individual assets in the portfolio.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.
    percentage (bool): If True, return risk contributions as percentages.

    Returns:
    np.ndarray: Array of risk contributions.
    """
    rc = np.dot(cov_matrix, weights) * weights
    if percentage:
        return rc / portfolio_vol(weights, cov_matrix)
    return rc


def portfolio_sharpe(
    weights: Union[np.ndarray, pd.Series],
    returns: Union[np.ndarray, pd.Series],
    cov_matrix: Union[np.ndarray, pd.DataFrame],
    risk_free: float = 0.0,
) -> float:
    """Calculate the Sharpe ratio of the portfolio.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    exp_returns (np.ndarray): Array of expected returns for each asset.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.
    risk_free (float): The risk-free rate.

    Returns:
    float: Sharpe ratio.
    """
    ret = portfolio_ret(weights, returns)
    vol = portfolio_vol(weights, cov_matrix)
    return (ret - risk_free) / vol


def portfolio_exante_te(
    weights1: Union[np.ndarray, pd.Series],
    weights2: Union[np.ndarray, pd.Series],
    cov_matrix: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the ex-ante tracking error between two portfolios.

    Parameters:
    weights1 (np.ndarray): Array of weights for the first portfolio.
    weights2 (np.ndarray): Array of weights for the second portfolio.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.

    Returns:
    float: Ex-ante tracking error.
    """
    active_weights = np.subtract(weights1, weights2)
    return portfolio_vol(active_weights, cov_matrix)
