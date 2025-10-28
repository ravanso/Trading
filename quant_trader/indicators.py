"""
Technical Indicators Module
============================

Provides technical analysis indicators for market analysis and feature engineering.
Used by the RL agent to make trading decisions.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional


def sma(data: Union[pd.Series, np.ndarray], period: int) -> Union[pd.Series, np.ndarray]:
    """
    Calculate Simple Moving Average.
    
    Args:
        data: Price data (Series or array)
        period: Number of periods for moving average
        
    Returns:
        SMA values
    """
    if isinstance(data, pd.Series):
        return data.rolling(window=period).mean()
    else:
        return pd.Series(data).rolling(window=period).mean().values


def ema(data: Union[pd.Series, np.ndarray], period: int) -> Union[pd.Series, np.ndarray]:
    """
    Calculate Exponential Moving Average.
    
    Args:
        data: Price data
        period: Number of periods
        
    Returns:
        EMA values
    """
    if isinstance(data, pd.Series):
        return data.ewm(span=period, adjust=False).mean()
    else:
        return pd.Series(data).ewm(span=period, adjust=False).mean().values


def rsi(data: Union[pd.Series, np.ndarray], period: int = 14) -> Union[pd.Series, np.ndarray]:
    """
    Calculate Relative Strength Index.
    
    Args:
        data: Price data
        period: RSI period (default: 14)
        
    Returns:
        RSI values (0-100)
    """
    if isinstance(data, np.ndarray):
        data = pd.Series(data)
    
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi_values = 100 - (100 / (1 + rs))
    
    return rsi_values if isinstance(data, pd.Series) else rsi_values.values


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: ATR period (default: 14)
        
    Returns:
        ATR values
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_values = tr.rolling(window=period).mean()
    
    return atr_values


def bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2.0) -> tuple:
    """
    Calculate Bollinger Bands.
    
    Args:
        data: Price data
        period: Moving average period
        std_dev: Number of standard deviations
        
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    middle_band = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return upper_band, middle_band, lower_band


def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        data: Price data
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
        
    Returns:
        Tuple of (macd_line, signal_line, histogram)
    """
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def iv_rank(current_iv: float, iv_history: pd.Series, period: int = 252) -> float:
    """
    Calculate IV Rank (Implied Volatility Rank).
    
    Args:
        current_iv: Current implied volatility
        iv_history: Historical IV values
        period: Period for calculation (default: 252 trading days)
        
    Returns:
        IV Rank (0-100)
    """
    iv_recent = iv_history.tail(period)
    iv_min = iv_recent.min()
    iv_max = iv_recent.max()
    
    if iv_max == iv_min:
        return 50.0
    
    iv_rank_value = ((current_iv - iv_min) / (iv_max - iv_min)) * 100
    return iv_rank_value


def support_resistance(data: pd.Series, window: int = 20, threshold: float = 0.02) -> dict:
    """
    Identify support and resistance levels.
    
    Args:
        data: Price data
        window: Window for local extrema
        threshold: Threshold for grouping similar levels
        
    Returns:
        Dict with 'support' and 'resistance' levels
    """
    # Find local maxima (resistance) and minima (support)
    local_max = data.rolling(window=window, center=True).max()
    local_min = data.rolling(window=window, center=True).min()
    
    resistance_levels = data[data == local_max].unique()
    support_levels = data[data == local_min].unique()
    
    # Group similar levels
    def group_levels(levels, threshold):
        if len(levels) == 0:
            return []
        grouped = []
        levels_sorted = sorted(levels)
        current_group = [levels_sorted[0]]
        
        for level in levels_sorted[1:]:
            if (level - current_group[-1]) / current_group[-1] <= threshold:
                current_group.append(level)
            else:
                grouped.append(np.mean(current_group))
                current_group = [level]
        grouped.append(np.mean(current_group))
        
        return grouped
    
    return {
        'support': group_levels(support_levels, threshold),
        'resistance': group_levels(resistance_levels, threshold)
    }

