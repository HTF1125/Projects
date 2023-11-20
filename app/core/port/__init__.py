from typing import Union
import numpy as np
import pandas as pd


def RET(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_ret: Union[np.ndarray, pd.Series],
) -> float:
    """Calculate the portfolio return.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    returns (np.ndarray): Array of asset returns.

    Returns:
    float: Portfolio return.
    """
    return np.dot(asset_wei, asset_ret)


def VAR(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_cov: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the portfolio variance.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.

    Returns:
    float: Portfolio variance.
    """
    return np.linalg.multi_dot((asset_wei, asset_cov, asset_wei))


def VOL(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_cov: Union[np.ndarray, pd.DataFrame],
) -> float:
    return VAR(asset_wei=asset_wei, asset_cov=asset_cov) ** 0.5


def COR(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_cor: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the portfolio correlation.

    Parameters:
    weights (np.ndarray): Array of portfolio weights for each asset.
    cor_matrix (np.ndarray): Correlation matrix of asset returns.

    Returns:
    float: Portfolio correlation.
    """
    return np.linalg.multi_dot((asset_wei, asset_cor, asset_wei))


def MarginalVol(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_cov: Union[np.ndarray, pd.DataFrame],
    as_pct: bool = True,
) -> np.ndarray:
    rc = np.dot(asset_cov, asset_wei) * asset_wei
    if as_pct:
        return rc / VOL(asset_wei, asset_cov)
    return rc


def Sharpe(
    asset_wei: Union[np.ndarray, pd.Series],
    asset_roi: Union[np.ndarray, pd.Series],
    asset_cov: Union[np.ndarray, pd.DataFrame],
    risk_free: float = 0.0,
) -> float:
    ret = RET(asset_wei, asset_roi)
    vol = VOL(asset_wei, asset_cov)
    return (ret - risk_free) / vol


def ExAnteTE(
    asset_wei1: Union[np.ndarray, pd.Series],
    asset_wei2: Union[np.ndarray, pd.Series],
    asset_cov: Union[np.ndarray, pd.DataFrame],
) -> float:
    """Calculate the ex-ante tracking error between two portfolios.

    Parameters:
    weights1 (np.ndarray): Array of weights for the first portfolio.
    weights2 (np.ndarray): Array of weights for the second portfolio.
    cov_matrix (np.ndarray): Covariance matrix of asset returns.

    Returns:
    float: Ex-ante tracking error.
    """
    active_wei = np.subtract(asset_wei1, asset_wei2)
    return VOL(asset_wei=active_wei, asset_cov=asset_cov)