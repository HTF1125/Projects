"""ROBERT"""
import numpy as np

def calculate_norm(array: np.ndarray, p: int = 1, gamma: float = 1.0) -> float:
    """
    Calculate the p-norm of a vector.

    The p-norm of a vector is the pth root of the sum of the pth powers of its components.
    Mathematically, for a vector x = (x₁, x₂, ..., xₙ), the p-norm is calculated as:
    ||x||ₚ = (∑(|xᵢ|ᵖ))^(1/p)

    Parameters:
    array (np.ndarray): Input vector.
    p (int): The value of p for the p-norm. Default is 1 (L1 norm).
    gamma (float): A scalar multiplier for the computed norm. Default is 1.

    Returns:
    float: Computed p-norm of the input vector, optionally scaled by gamma.
    """
    norm_value = np.power(np.sum(np.power(np.abs(array), p)), 1 / p)
    return norm_value * gamma


def l1_norm(array: np.ndarray, gamma: float = 1.0) -> float:
    """this is a pass through function"""
    return calculate_norm(array=array, p=1, gamma=gamma)


def l2_norm(array: np.ndarray, gamma: float = 1.0) -> float:
    """this is a pass through function"""
    return calculate_norm(array=array, p=2, gamma=gamma)


def l3_norm(array: np.ndarray, gamma: float = 1.0) -> float:
    """this is a pass through function"""
    return calculate_norm(array=array, p=3, gamma=gamma)


def l4_norm(array: np.ndarray, gamma: float = 1.0) -> float:
    """this is a pass through function"""
    return calculate_norm(array=array, p=4, gamma=gamma)
