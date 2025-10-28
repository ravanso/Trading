"""
Risk Management Module
======================

Handles position sizing, risk limits, and portfolio risk management.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


class RiskManager:
    """
    Risk management system for portfolio and position-level risk control.
    """
    
    def __init__(
        self,
        max_position_size: float = 0.02,  # 2% per trade
        max_portfolio_heat: float = 0.10,  # 10% total at risk
        max_drawdown: float = 0.20,  # 20% max drawdown
        max_daily_loss: float = 0.05  # 5% max daily loss
    ):
        """
        Initialize risk manager.
        
        Args:
            max_position_size: Maximum risk per position (as fraction of capital)
            max_portfolio_heat: Maximum total portfolio risk
            max_drawdown: Maximum allowable drawdown
            max_daily_loss: Maximum daily loss limit
        """
        self.max_position_size = max_position_size
        self.max_portfolio_heat = max_portfolio_heat
        self.max_drawdown = max_drawdown
        self.max_daily_loss = max_daily_loss
        
        self.current_heat = 0.0
        self.daily_pnl = 0.0
        self.peak_equity = 0.0
        
    def calculate_position_size(
        self,
        capital: float,
        entry_price: float,
        stop_loss: float,
        method: str = "fixed_risk"
    ) -> int:
        """
        Calculate position size based on risk parameters.
        
        Args:
            capital: Available capital
            entry_price: Entry price per contract
            stop_loss: Stop loss price
            method: Position sizing method
            
        Returns:
            Number of contracts to trade
        """
        if method == "fixed_risk":
            risk_amount = capital * self.max_position_size
            risk_per_contract = abs(entry_price - stop_loss)
            
            if risk_per_contract == 0:
                return 0
            
            position_size = int(risk_amount / risk_per_contract)
            return max(1, position_size)
        
        elif method == "kelly_criterion":
            # Simplified Kelly criterion
            # Requires win_rate and avg_win/loss data
            # TODO: Implement full Kelly criterion
            return int(capital * self.max_position_size / entry_price)
        
        else:
            # Fixed fractional
            return int((capital * self.max_position_size) / entry_price)
    
    def check_position_allowed(
        self,
        position_risk: float,
        capital: float,
        current_positions: int = 0
    ) -> tuple[bool, str]:
        """
        Check if new position is allowed based on risk limits.
        
        Args:
            position_risk: Risk of proposed position (max loss)
            capital: Current capital
            current_positions: Number of existing positions
            
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        # Check individual position size
        position_risk_pct = position_risk / capital
        if position_risk_pct > self.max_position_size:
            return False, "Position size exceeds maximum risk per trade" + \
                          " (" + str(round(position_risk_pct * 100, 2)) + "% vs " + \
                          str(self.max_position_size * 100) + "% limit)"
        
        # Check total portfolio heat
        new_total_heat = self.current_heat + position_risk_pct
        if new_total_heat > self.max_portfolio_heat:
            return False, "Would exceed maximum portfolio heat" + \
                          " (" + str(round(new_total_heat * 100, 2)) + "% vs " + \
                          str(self.max_portfolio_heat * 100) + "% limit)"
        
        # Check daily loss limit
        daily_loss_pct = abs(self.daily_pnl) / capital if self.daily_pnl < 0 else 0
        if daily_loss_pct > self.max_daily_loss:
            return False, "Daily loss limit reached" + \
                          " (" + str(round(daily_loss_pct * 100, 2)) + "%)"
        
        return True, "Position allowed"
    
    def update_risk_metrics(
        self,
        current_equity: float,
        daily_pnl: float,
        open_position_risk: float
    ) -> None:
        """
        Update risk tracking metrics.
        
        Args:
            current_equity: Current portfolio equity
            daily_pnl: Today's P&L
            open_position_risk: Total risk from open positions
        """
        self.daily_pnl = daily_pnl
        self.current_heat = open_position_risk / current_equity
        
        # Update peak equity for drawdown calculation
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity
    
    def check_circuit_breaker(self, current_equity: float) -> tuple[bool, str]:
        """
        Check if circuit breakers should be triggered.
        
        Args:
            current_equity: Current portfolio equity
            
        Returns:
            Tuple of (triggered: bool, reason: str)
        """
        # Check drawdown
        if self.peak_equity > 0:
            drawdown = (self.peak_equity - current_equity) / self.peak_equity
            if drawdown > self.max_drawdown:
                return True, "Maximum drawdown exceeded: " + str(round(drawdown * 100, 2)) + "%"
        
        # Check daily loss
        if self.peak_equity > 0:
            daily_loss_pct = abs(self.daily_pnl / self.peak_equity)
            if self.daily_pnl < 0 and daily_loss_pct > self.max_daily_loss:
                return True, "Daily loss limit exceeded: " + str(round(daily_loss_pct * 100, 2)) + "%"
        
        return False, "No circuit breakers triggered"


def calculate_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR).
    
    Args:
        returns: Return series
        confidence_level: Confidence level (default: 95%)
        
    Returns:
        VaR value
    """
    return np.percentile(returns, (1 - confidence_level) * 100)


def calculate_cvar(returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Conditional Value at Risk (CVaR) / Expected Shortfall.
    
    Args:
        returns: Return series
        confidence_level: Confidence level
        
    Returns:
        CVaR value
    """
    var = calculate_var(returns, confidence_level)
    return returns[returns <= var].mean()


def kelly_criterion(
    win_rate: float,
    avg_win: float,
    avg_loss: float,
    fraction: float = 0.25
) -> float:
    """
    Calculate Kelly Criterion for position sizing.
    
    Args:
        win_rate: Probability of winning (0-1)
        avg_win: Average win amount
        avg_loss: Average loss amount
        fraction: Fraction of Kelly to use (default: 0.25 for safety)
        
    Returns:
        Recommended position size (as fraction of capital)
    """
    if avg_loss == 0:
        return 0.0
    
    b = avg_win / avg_loss  # Win/loss ratio
    p = win_rate
    q = 1 - p
    
    kelly = (p * b - q) / b
    
    # Apply fractional Kelly for safety
    return max(0, min(kelly * fraction, 0.25))  # Cap at 25%


def calculate_greeks_risk(positions: list) -> Dict[str, float]:
    """
    Calculate portfolio-level Greeks risk exposure.
    
    Args:
        positions: List of positions with Greeks
        
    Returns:
        Dictionary of aggregated Greeks
    """
    total_greeks = {
        'delta': 0.0,
        'gamma': 0.0,
        'theta': 0.0,
        'vega': 0.0,
        'rho': 0.0
    }
    
    for position in positions:
        greeks = position.get('greeks', {})
        quantity = position.get('quantity', 0)
        
        for greek in total_greeks:
            if greek in greeks:
                total_greeks[greek] += greeks[greek] * quantity
    
    return total_greeks


def calculate_correlation_risk(returns: pd.DataFrame, threshold: float = 0.7) -> Dict:
    """
    Calculate correlation risk between positions.
    
    Args:
        returns: DataFrame of position returns
        threshold: Correlation threshold for warning
        
    Returns:
        Dictionary with correlation analysis
    """
    corr_matrix = returns.corr()
    
    # Find highly correlated pairs
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > threshold:
                high_corr_pairs.append({
                    'asset1': corr_matrix.columns[i],
                    'asset2': corr_matrix.columns[j],
                    'correlation': corr_value
                })
    
    return {
        'correlation_matrix': corr_matrix,
        'high_correlation_pairs': high_corr_pairs,
        'max_correlation': corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].max(),
        'diversification_ratio': len(returns.columns) / corr_matrix.values.mean()
    }

