"""ROBERT"""
import warnings
from typing import Union, overload, Optional, Tuple
import pandas as pd


####################################################################################################
# Standard Scaler
####################################################################################################
@overload
def standard_scaler(
    data: pd.Series,
    axis: int = 0,
    bounds: Optional[Tuple] = None,
) -> pd.Series:
    ...


@overload
def standard_scaler(
    data: pd.DataFrame,
    axis: int = 0,
    bounds: Optional[Tuple] = None,
) -> pd.DataFrame:
    ...


def standard_scaler(
    data: Union[pd.Series, pd.DataFrame],
    axis: int = 0,
    bounds: Optional[Tuple] = None,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate standard scaling for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate standard scaling.
    axis (int): The axis along which to calculate the scaling (0 for rows, 1 for columns). Default is 0.

    Returns:
    Union[pd.Series, pd.DataFrame]: Standard-scaled data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, apply standard scaling along the specified axis
        return data.aggregate(
            func=standard_scaler,
            axis="index" if axis == 0 else "columns",
        )
    # If the input is a Series, calculate standard scaling for the Series
    scaler = (data - data.mean()) / data.std()

    if bounds:
        if isinstance(range, tuple):
            min_bound, max_bound = bounds
            scaler = min_bound + (scaler - scaler.min()) * (max_bound - min_bound) / (
                scaler.max() - scaler.min()
            )
            return scaler
        warnings.warn(message="the range must be a tuple of float. i.e. (0., 1.)")
    return scaler


####################################################################################################
# Robust Scaler
####################################################################################################


@overload
def robust_scaler(
    data: pd.Series,
    axis: int = 0,
) -> pd.Series:
    ...


@overload
def robust_scaler(
    data: pd.DataFrame,
    axis: int = 0,
) -> pd.DataFrame:
    ...


def robust_scaler(
    data: Union[pd.Series, pd.DataFrame],
    axis: int = 0,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate robust scaling for a pandas Series or DataFrame.

    Robust scaling (also known as robust normalization) is a method of scaling features to be robust
    against the presence of outliers. It subtracts the median and scales the data by the
    interquartile range (IQR).

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate robust scaling.
    axis (int): The axis along which to calculate the scaling (0 for rows, 1 for columns). Default is 0.

    Returns:
    Union[pd.Series, pd.DataFrame]: Robust-scaled data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, apply robust scaling along the specified axis
        return data.aggregate(
            func=robust_scaler,
            axis="index" if axis == 0 else "columns",
        )
    quantile1 = data.quantile(q=0.25)
    quantile3 = data.quantile(q=0.75)
    median = data.median()
    return (data - median) / (quantile3 - quantile1)


####################################################################################################
# MinMax Scaler
####################################################################################################
@overload
def min_max_scaler(
    data: pd.Series,
    axis: int = 0,
) -> pd.Series:
    ...


@overload
def min_max_scaler(
    data: pd.DataFrame,
    axis: int = 0,
) -> pd.DataFrame:
    ...


def min_max_scaler(
    data: Union[pd.Series, pd.DataFrame],
    axis: int = 0,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate min-max scaling for a pandas Series or DataFrame.

    Min-max scaling (also known as min-max normalization) is a method of scaling features to a specific
    range, typically between 0 and 1. It scales the data by subtracting the minimum value and dividing
    by the range (maximum - minimum).

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate min-max scaling.
    axis (int): The axis along which to calculate the scaling (0 for rows, 1 for columns). Default is 0.

    Returns:
    Union[pd.Series, pd.DataFrame]: Min-max scaled data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, apply min-max scaling along the specified axis
        return data.aggregate(
            func=min_max_scaler,
            axis="index" if axis == 0 else "columns",
        )
    minimum, maximum = data.min(), data.max()
    return (data - minimum) / (maximum - minimum)


####################################################################################################
# BoxCox Scaler
####################################################################################################
def box_cox_scaler():
    """
    Box-Cox Trasformation is a statistical technique that transforms
    the data so that it closely reseble a normal distribution.

    In many statistical techniques, we assume that the errors are
    normally distributed. This assumption allows us to construct
    confidence intervals and conduct hypothesis tests. By transforming
    your target variable, we can hopefully normalize our errors, if
    they are not already normal.
    """
    ...
