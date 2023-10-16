"""ROBERT"""
from typing import Union
from typing import overload
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


####################################################################################################
# Price Return
####################################################################################################
@overload
def pri_return(
    data: pd.Series,
    periods: int = 1,
    forward: bool = False,
) -> pd.Series:
    ...


@overload
def pri_return(
    data: pd.DataFrame,
    periods: int = 1,
    forward: bool = False,
) -> pd.DataFrame:
    ...


def pri_return(
    data: Union[pd.Series, pd.DataFrame],
    periods: int = 1,
    forward: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate percentage returns for a given time series data.

    Args:
        data (Union[pd.Series, pd.DataFrame]): Input time series data.
        periods (int, optional): Number of periods to shift. Default is 1.
        freq (Optional[pd.DateOffset], optional): Frequency of the data. Default is None.
        forward (bool, optional): If True, shift data forward; if False, shift data backward. Default is False.

    Returns:
        Union[pd.Series, pd.DataFrame]: Percentage returns.
    """
    if not isinstance(data, (pd.Series, pd.DataFrame)):
        raise ValueError("Input data must be a pandas Series or DataFrame")
    return data.pct_change(periods=periods).shift(periods=-periods if forward else 0)


####################################################################################################
# Logrithmic Return
####################################################################################################
@overload
def log_return(
    data: pd.Series,
    periods: int = 1,
    forward: bool = False,
) -> pd.Series:
    ...


@overload
def log_return(
    data: pd.DataFrame,
    periods: int = 1,
    forward: bool = False,
) -> pd.DataFrame:
    ...


def log_return(
    data: Union[pd.Series, pd.DataFrame],
    periods: int = 1,
    forward: bool = False,
) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate log returns for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate log returns.
    periods (int): Number of periods to calculate returns for.
    forward (bool): If True, calculate forward returns; if False, calculate backward returns.

    Returns:
    Union[pd.Series, pd.DataFrame]: Log returns calculated for the input data.
    """
    return pri_return(data=data, periods=periods, forward=forward).apply(np.log1p)


####################################################################################################
# Cumulative Return
####################################################################################################
@overload
def cum_return(data: pd.Series) -> pd.Series:
    ...


# This overload handles a pandas DataFrame
@overload
def cum_return(data: pd.DataFrame) -> pd.DataFrame:
    ...


def cum_return(data: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate cumulative return for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate cumulative returns.

    Returns:
    Union[pd.Series, pd.DataFrame]: Cumulative return calculated for the input data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, apply cum_return to each column
        out = data.aggregate(cum_return)
        out.name = "Cum.Return"
        return out
    # If the input is a Series, calculate cumulative return for the Series
    data = data.dropna()  # Remove NaN values
    return data.iloc[-1] / data.iloc[0] - 1


####################################################################################################
# Annualized Return
####################################################################################################
@overload
def ann_return(
    data: pd.DataFrame,
    ann_factor: Union[int, float] = 252,
) -> pd.Series:
    ...


@overload
def ann_return(
    data: pd.Series,
    ann_factor: Union[int, float] = 252,
) -> float:
    ...


def ann_return(
    data: Union[pd.Series, pd.DataFrame],
    ann_factor: Union[int, float] = 252,
) -> Union[pd.Series, float]:
    """
    Calculate annualized return for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate annualized return.
    ann_factor (Union[int, float]): Annualization factor (e.g., 252 for daily data).

    Returns:
    Union[pd.Series, float]: Annualized return calculated for the input data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, calculate the annualized return for each column
        out = data.aggregate(ann_return, axis=0, ann_factor=ann_factor)
        out.name = "Ann.Return"
        return out
    # If the input is a Series, calculate the annualized return for the Series
    base_return = np.exp(log_return(data).mean()) - 1
    return base_return * ann_factor


####################################################################################################
# Annualized Volatility
####################################################################################################
@overload
def ann_volatility(
    data: pd.DataFrame,
    ann_factor: Union[int, float] = 252,
) -> pd.Series:
    ...


@overload
def ann_volatility(
    data: pd.Series,
    ann_factor: Union[int, float] = 252,
) -> float:
    ...


def ann_volatility(
    data: Union[pd.Series, pd.DataFrame],
    ann_factor: Union[int, float] = 252,
) -> Union[pd.Series, float]:
    """
    Calculate annualized return for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate annualized return.
    ann_factor (Union[int, float]): Annualization factor (e.g., 252 for daily data).

    Returns:
    Union[pd.Series, float]: Annualized return calculated for the input data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, calculate the annualized return for each column
        out = data.aggregate(ann_volatility, axis=0, ann_factor=ann_factor)
        out.name = "Ann.Volatility"
        return out
    # If the input is a Series, calculate the annualized return for the Series
    base_return = log_return(data).std()
    return base_return * ann_factor**0.5


####################################################################################################
# Annualized Sharpe
####################################################################################################
@overload
def ann_sharpe(
    data: pd.DataFrame,
    risk_free: float = 0.0,
    ann_factor: Union[int, float] = 252,
) -> pd.Series:
    ...


@overload
def ann_sharpe(
    data: pd.Series,
    risk_free: float = 0.0,
    ann_factor: Union[int, float] = 252,
) -> float:
    ...


def ann_sharpe(
    data: Union[pd.Series, pd.DataFrame],
    risk_free: float = 0.0,
    ann_factor: Union[int, float] = 252,
) -> Union[pd.Series, float]:
    """
    Calculate annualized return for a pandas Series or DataFrame.

    Parameters:
    data (Union[pd.Series, pd.DataFrame]): Input data for which to calculate annualized return.
    ann_factor (Union[int, float]): Annualization factor (e.g., 252 for daily data).

    Returns:
    Union[pd.Series, float]: Annualized return calculated for the input data.
    """
    if isinstance(data, pd.DataFrame):
        # If the input is a DataFrame, calculate the annualized return for each column
        out = data.aggregate(ann_sharpe, axis=0, ann_factor=ann_factor)
        out.name = "Ann.Sharpe"
        return out
    # If the input is a Series, calculate the annualized return for the Series
    return (ann_return(data) - risk_free) / ann_volatility(data)


####################################################################################################
# Information Ratio
####################################################################################################


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
    combined_data = pd.concat([forward_returns.stack(), factor_data.stack()], axis=1)
    combined_data = combined_data.dropna().reset_index()
    combined_data.columns = ["Date", "Ticker", "Factor", "Return"]

    # Calculate information coefficient for each date
    info_coefficient = combined_data.groupby("Date").apply(
        lambda x: spearmanr(a=x["Factor"], b=x["Return"])[0]
    )
    info_coefficient.name = "Info.Coefficient"

    return info_coefficient


####################################################################################################
# Uncategorized
####################################################################################################
def MA(
    data: Union[pd.Series, pd.DataFrame], window: int = 5
) -> Union[pd.Series, pd.DataFrame]:
    return data.rolling(window=window).mean()


def EMA(
    data: Union[pd.Series, pd.DataFrame], window: int = 5
) -> Union[pd.Series, pd.DataFrame]:
    return data.ewm(span=window).mean()


def MACD(
    data: Union[pd.Series, pd.DataFrame],
    window1: int = 12,
    window2: int = 26,
    window3: int = 9,
) -> Union[pd.Series, pd.DataFrame]:
    ema1 = EMA(data=data, window=window1)
    ema2 = EMA(data=data, window=window2)
    macd = ema1 - ema2
    macd_s = EMA(data=macd, window=window3)
    return macd_s - macd
