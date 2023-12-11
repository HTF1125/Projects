"""ROBERT"""
import warnings
from typing import Optional, Tuple
import pandas as pd


def StandardScaler(data: pd.Series, zero_aware: bool = False) -> pd.Series:
    mean = 0 if zero_aware else data.mean()
    return (data - mean) / data.std()


def RobustScaler(
    data: pd.Series,
) -> pd.Series:
    quantile1 = data.quantile(q=0.25)
    quantile3 = data.quantile(q=0.75)
    median = data.median()
    return (data - median) / (quantile3 - quantile1)


def MinMaxScaler(
    data: pd.Series,
) -> pd.Series:
    minimum, maximum = data.min(), data.max()
    return (data - minimum) / (maximum - minimum)


def BoxCoxScaler():
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
