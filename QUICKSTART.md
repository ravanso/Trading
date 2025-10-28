# Quick Start Guide

## Installation

```bash
# Clone and enter directory
git clone https://github.com/ravanso/Trading.git
cd Trading

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install as editable package
pip install -e .
```

## Basic Usage

### 1. Import the Package
```python
import quant_trader as qt
```

### 2. Use Technical Indicators
```python
import pandas as pd
import numpy as np

# Sample price data
prices = pd.Series(np.random.randn(100).cumsum() + 100)

# Calculate indicators
rsi = qt.indicators.rsi(prices, period=14)
sma_20 = qt.indicators.sma(prices, period=20)
upper, middle, lower = qt.indicators.bollinger_bands(prices)
```

### 3. Portfolio Management
```python
# Create portfolio
portfolio = qt.portfolio.Portfolio(initial_capital=100000)

# Check portfolio status
print("Total Value: " + str(portfolio.total_value))
print("P&L: " + str(portfolio.pnl))
print("P&L %: " + str(portfolio.pnl_percent))

# Get portfolio Greeks
greeks = portfolio.get_portfolio_greeks()
print(greeks)
```

### 4. Risk Management
```python
# Initialize risk manager
risk_mgr = qt.risk.RiskManager(
    max_position_size=0.02,  # 2% per trade
    max_portfolio_heat=0.10   # 10% total risk
)

# Calculate position size
position_size = risk_mgr.calculate_position_size(
    capital=100000,
    entry_price=5.00,
    stop_loss=4.50
)

# Check if position is allowed
allowed, reason = risk_mgr.check_position_allowed(
    position_risk=1000,
    capital=100000
)
print("Position allowed: " + str(allowed) + " - " + reason)
```

### 5. Calculate Options Greeks
```python
from quant_trader.utils import greeks

# Calculate all Greeks for an option
option_greeks = greeks.calculate_all_greeks(
    S=100,      # Stock price
    K=105,      # Strike price
    T=0.25,     # Time to expiration (years)
    r=0.05,     # Risk-free rate
    sigma=0.20, # Volatility
    option_type="call"
)

print(option_greeks)
# Output: {'price': 2.45, 'delta': 0.42, 'gamma': 0.03, 'theta': -0.05, 'vega': 0.15, 'rho': 0.08}
```

### 6. Portfolio Optimization
```python
# Create sample returns data
returns = pd.DataFrame(np.random.randn(252, 5), columns=['A', 'B', 'C', 'D', 'E'])

# Optimize portfolio weights
weights = qt.portfolio.optimize_portfolio(returns, method="mean_variance")
print("Optimal weights: " + str(weights))

# Calculate Sharpe ratio
sharpe = qt.portfolio.calculate_sharpe_ratio(returns['A'])
print("Sharpe Ratio: " + str(sharpe))
```

## Package Structure

```
import quant_trader as qt

# Core modules
qt.indicators     # Technical indicators (RSI, SMA, MACD, etc.)
qt.portfolio      # Portfolio management and tracking
qt.backtest       # Backtesting framework
qt.risk           # Risk management and position sizing

# Sub-modules
qt.data           # Data collection and processing
qt.agents         # RL agents (PPO, A2C, SAC)
qt.strategies     # Trading strategies (vertical spreads, iron condors)
qt.utils          # Utilities (Greeks calculations, helpers)
```

## Common Functions Reference

### Indicators
```python
qt.indicators.sma(data, period)          # Simple Moving Average
qt.indicators.ema(data, period)          # Exponential Moving Average
qt.indicators.rsi(data, period=14)       # Relative Strength Index
qt.indicators.atr(high, low, close, 14)  # Average True Range
qt.indicators.bollinger_bands(data, 20)  # Bollinger Bands
qt.indicators.macd(data, 12, 26, 9)      # MACD
qt.indicators.iv_rank(current_iv, history)  # IV Rank
```

### Portfolio
```python
portfolio = qt.portfolio.Portfolio(initial_capital)
portfolio.add_position(position)
portfolio.close_position(idx, exit_price, exit_date)
portfolio.get_portfolio_greeks()
portfolio.get_metrics()

qt.portfolio.optimize_portfolio(returns, method)
qt.portfolio.calculate_sharpe_ratio(returns)
qt.portfolio.calculate_max_drawdown(equity_curve)
```

### Risk Management
```python
risk_mgr = qt.risk.RiskManager(max_position_size, max_portfolio_heat)
risk_mgr.calculate_position_size(capital, entry, stop)
risk_mgr.check_position_allowed(risk, capital)
risk_mgr.check_circuit_breaker(equity)

qt.risk.calculate_var(returns, confidence=0.95)
qt.risk.kelly_criterion(win_rate, avg_win, avg_loss)
```

### Greeks
```python
from quant_trader.utils import greeks

greeks.black_scholes_price(S, K, T, r, sigma, type)
greeks.calculate_delta(S, K, T, r, sigma, type)
greeks.calculate_gamma(S, K, T, r, sigma)
greeks.calculate_theta(S, K, T, r, sigma, type)
greeks.calculate_vega(S, K, T, r, sigma)
greeks.calculate_all_greeks(S, K, T, r, sigma, type)
```

## Examples

### Example 1: Simple Backtest Setup
```python
import quant_trader as qt
import pandas as pd

# Load data
data = pd.read_csv('historical_data.csv')

# Initialize backtest
backtest = qt.backtest.Backtest(
    data=data,
    initial_capital=100000,
    commission=0.65,
    slippage=0.05
)

# Run backtest (implement your strategy function)
# results = backtest.run(my_strategy)

# Get metrics
metrics = backtest.get_metrics()
print(metrics)
```

### Example 2: Risk-Managed Trade
```python
import quant_trader as qt

# Setup
capital = 100000
risk_mgr = qt.risk.RiskManager(max_position_size=0.02)

# Trade parameters
entry_price = 5.00
stop_loss = 4.50

# Calculate position size
size = risk_mgr.calculate_position_size(capital, entry_price, stop_loss)

# Check if allowed
allowed, reason = risk_mgr.check_position_allowed(
    position_risk=size * (entry_price - stop_loss),
    capital=capital
)

if allowed:
    print("Trade " + str(size) + " contracts")
else:
    print("Trade rejected: " + reason)
```

## Next Steps

1. Review full documentation in markdown files
2. Explore example notebooks (coming soon)
3. Start building your first strategy
4. Train your first RL agent

## Support

- Documentation: See `.md` files in repository
- Issues: https://github.com/ravanso/Trading/issues

