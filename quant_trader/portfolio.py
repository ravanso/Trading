"""
Portfolio Management Module
============================

Handles portfolio tracking, position management, and portfolio optimization.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Position:
    """Represents a trading position."""
    symbol: str
    strategy_type: str  # e.g., "vertical_spread", "iron_condor"
    entry_date: datetime
    entry_price: float
    quantity: int
    strikes: List[float]
    expiration: datetime
    position_type: str  # "long" or "short"
    greeks: Dict[str, float]  # Delta, Gamma, Theta, Vega
    max_loss: float
    max_profit: float
    current_value: float = 0.0
    pnl: float = 0.0


class Portfolio:
    """
    Portfolio management class for tracking positions and performance.
    """
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize portfolio.
        
        Args:
            initial_capital: Starting capital
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.trade_history: List[Dict] = []
        
    @property
    def total_value(self) -> float:
        """Calculate total portfolio value."""
        positions_value = sum(pos.current_value for pos in self.positions)
        return self.cash + positions_value
    
    @property
    def equity(self) -> float:
        """Calculate portfolio equity."""
        return self.total_value
    
    @property
    def pnl(self) -> float:
        """Calculate total P&L."""
        return self.total_value - self.initial_capital
    
    @property
    def pnl_percent(self) -> float:
        """Calculate P&L percentage."""
        return (self.pnl / self.initial_capital) * 100
    
    def add_position(self, position: Position) -> None:
        """Add a new position to the portfolio."""
        self.positions.append(position)
        self.cash -= position.entry_price * position.quantity
        
    def close_position(self, position_idx: int, exit_price: float, exit_date: datetime) -> float:
        """
        Close a position and calculate P&L.
        
        Args:
            position_idx: Index of position to close
            exit_price: Exit price
            exit_date: Exit date
            
        Returns:
            P&L from the trade
        """
        position = self.positions[position_idx]
        pnl = (exit_price - position.entry_price) * position.quantity
        
        if position.position_type == "short":
            pnl = -pnl
        
        position.pnl = pnl
        self.cash += exit_price * position.quantity + pnl
        
        # Move to closed positions
        self.closed_positions.append(position)
        self.positions.pop(position_idx)
        
        # Record trade
        self.trade_history.append({
            'symbol': position.symbol,
            'strategy': position.strategy_type,
            'entry_date': position.entry_date,
            'exit_date': exit_date,
            'entry_price': position.entry_price,
            'exit_price': exit_price,
            'pnl': pnl,
            'pnl_percent': (pnl / (position.entry_price * position.quantity)) * 100
        })
        
        return pnl
    
    def update_positions(self, market_data: Dict) -> None:
        """Update current values of all positions based on market data."""
        for position in self.positions:
            if position.symbol in market_data:
                position.current_value = market_data[position.symbol]['price']
                position.greeks = market_data[position.symbol].get('greeks', position.greeks)
                
                pnl = (position.current_value - position.entry_price) * position.quantity
                if position.position_type == "short":
                    pnl = -pnl
                position.pnl = pnl
    
    def get_portfolio_greeks(self) -> Dict[str, float]:
        """Calculate portfolio-level Greeks."""
        portfolio_greeks = {
            'delta': 0.0,
            'gamma': 0.0,
            'theta': 0.0,
            'vega': 0.0
        }
        
        for position in self.positions:
            for greek in portfolio_greeks:
                if greek in position.greeks:
                    portfolio_greeks[greek] += position.greeks[greek] * position.quantity
        
        return portfolio_greeks
    
    def get_metrics(self) -> Dict[str, float]:
        """Calculate portfolio performance metrics."""
        if len(self.closed_positions) == 0:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0
            }
        
        trades = [pos.pnl for pos in self.closed_positions]
        wins = [pnl for pnl in trades if pnl > 0]
        losses = [pnl for pnl in trades if pnl < 0]
        
        metrics = {
            'total_trades': len(trades),
            'win_rate': len(wins) / len(trades) * 100 if trades else 0,
            'avg_win': np.mean(wins) if wins else 0,
            'avg_loss': abs(np.mean(losses)) if losses else 0,
            'profit_factor': sum(wins) / abs(sum(losses)) if losses else float('inf')
        }
        
        return metrics


def optimize_portfolio(returns: pd.DataFrame, method: str = "mean_variance") -> np.ndarray:
    """
    Optimize portfolio weights.
    
    Args:
        returns: DataFrame of asset returns
        method: Optimization method ("mean_variance", "risk_parity", "equal_weight")
        
    Returns:
        Optimal weights array
    """
    n_assets = returns.shape[1]
    
    if method == "equal_weight":
        return np.ones(n_assets) / n_assets
    
    elif method == "mean_variance":
        # Simple mean-variance optimization
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        # Max Sharpe ratio (simplified)
        inv_cov = np.linalg.pinv(cov_matrix)
        weights = inv_cov @ mean_returns
        weights = weights / weights.sum()
        
        return np.abs(weights) / np.abs(weights).sum()
    
    elif method == "risk_parity":
        # Equal risk contribution
        cov_matrix = returns.cov()
        weights = np.ones(n_assets) / n_assets
        
        # Iterative adjustment (simplified)
        for _ in range(100):
            portfolio_var = weights.T @ cov_matrix @ weights
            marginal_contrib = cov_matrix @ weights
            risk_contrib = weights * marginal_contrib / portfolio_var
            weights = weights * (1 / n_assets) / risk_contrib
            weights = weights / weights.sum()
        
        return weights
    
    else:
        raise ValueError("Unknown optimization method: " + str(method))


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe Ratio.
    
    Args:
        returns: Return series
        risk_free_rate: Annual risk-free rate (default: 2%)
        
    Returns:
        Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sortino Ratio (downside deviation).
    
    Args:
        returns: Return series
        risk_free_rate: Annual risk-free rate
        
    Returns:
        Sortino ratio
    """
    excess_returns = returns - (risk_free_rate / 252)
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = downside_returns.std()
    
    if downside_std == 0:
        return 0.0
    
    return np.sqrt(252) * excess_returns.mean() / downside_std


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    """
    Calculate maximum drawdown.
    
    Args:
        equity_curve: Equity curve series
        
    Returns:
        Maximum drawdown (as percentage)
    """
    cummax = equity_curve.cummax()
    drawdown = (equity_curve - cummax) / cummax
    return drawdown.min() * 100

