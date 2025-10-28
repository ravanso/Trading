"""
Quant Trader - AI-Powered Options Trading System
=================================================

A reinforcement learning-based options trading system that uses ML agents
to identify profitable opportunities and manage risk.

Modules:
    - data: Data collection and processing for options chains
    - agents: Reinforcement learning agents and training
    - strategies: Options trading strategies implementation
    - utils: Helper functions and utilities
    - indicators: Technical indicators and calculations
    - portfolio: Portfolio management and position tracking
    - backtest: Backtesting framework
    - risk: Risk management and position sizing
"""

__version__ = "0.1.0"
__author__ = "Rayan & Guillaume"

from quant_trader import indicators
from quant_trader import portfolio
from quant_trader import backtest
from quant_trader import risk

__all__ = [
    "indicators",
    "portfolio", 
    "backtest",
    "risk",
    "data",
    "agents",
    "strategies",
    "utils"
]

