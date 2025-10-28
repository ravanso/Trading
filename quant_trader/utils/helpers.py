"""
Helper Functions Module
=======================

General utility and helper functions.
"""

import pandas as pd
from datetime import datetime, timedelta


def calculate_dte(expiration_date: datetime) -> int:
    """
    Calculate Days To Expiration.
    
    Args:
        expiration_date: Option expiration date
        
    Returns:
        Days to expiration
    """
    today = datetime.now()
    return (expiration_date - today).days


def is_market_open() -> bool:
    """
    Check if market is currently open (simple check).
    
    Returns:
        True if market is open
    """
    now = datetime.now()
    
    # Check if weekend
    if now.weekday() >= 5:
        return False
    
    # Check market hours (9:30 AM - 4:00 PM ET)
    market_open = now.replace(hour=9, minute=30, second=0)
    market_close = now.replace(hour=16, minute=0, second=0)
    
    return market_open <= now <= market_close


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return "${:,.2f}".format(amount)


def format_percentage(value: float) -> str:
    """Format value as percentage string."""
    return "{:.2f}%".format(value)

