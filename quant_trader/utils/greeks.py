"""
Greeks Calculations Module
==========================

Calculate options Greeks (Delta, Gamma, Theta, Vega, Rho).
"""

import numpy as np
from scipy.stats import norm


def black_scholes_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call"
) -> float:
    """
    Calculate Black-Scholes option price.
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration (years)
        r: Risk-free rate
        sigma: Volatility (annualized)
        option_type: "call" or "put"
        
    Returns:
        Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return price


def calculate_delta(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call"
) -> float:
    """Calculate Delta."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option_type == "call":
        return norm.cdf(d1)
    else:  # put
        return norm.cdf(d1) - 1


def calculate_gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Calculate Gamma."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def calculate_theta(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call"
) -> float:
    """Calculate Theta (per day)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        theta = (
            -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        )
    else:  # put
        theta = (
            -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        )
    
    return theta / 365  # Convert to daily


def calculate_vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Calculate Vega (per 1% change in volatility)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) / 100


def calculate_rho(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call"
) -> float:
    """Calculate Rho (per 1% change in interest rate)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        return K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:  # put
        return -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100


def calculate_all_greeks(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call"
) -> dict:
    """
    Calculate all Greeks at once.
    
    Returns:
        Dictionary with all Greeks
    """
    return {
        'price': black_scholes_price(S, K, T, r, sigma, option_type),
        'delta': calculate_delta(S, K, T, r, sigma, option_type),
        'gamma': calculate_gamma(S, K, T, r, sigma),
        'theta': calculate_theta(S, K, T, r, sigma, option_type),
        'vega': calculate_vega(S, K, T, r, sigma),
        'rho': calculate_rho(S, K, T, r, sigma, option_type)
    }

