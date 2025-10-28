# Installation Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ravanso/Trading.git
cd Trading
```

### 2. Create Virtual Environment
```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Or using conda
conda create -n quant_trader python=3.10
conda activate quant_trader
```

### 3. Install Package in Editable Mode
```bash
# Install core dependencies
pip install -e .

# Or install with all extras
pip install -e ".[rl,options,brokers,viz,dev]"

# Or install from requirements.txt
pip install -r requirements.txt
```

## Package Structure

```
quant_trader/
├── __init__.py           # Main package initialization
├── indicators.py         # Technical indicators
├── portfolio.py          # Portfolio management
├── backtest.py          # Backtesting framework
├── risk.py              # Risk management
├── data/                # Data collection & processing
│   ├── __init__.py
│   ├── collectors.py
│   └── processors.py
├── agents/              # RL agents
│   ├── __init__.py
│   ├── rl_agent.py
│   └── training.py
├── strategies/          # Trading strategies
│   ├── __init__.py
│   ├── vertical_spreads.py
│   └── iron_condor.py
└── utils/               # Utilities
    ├── __init__.py
    ├── greeks.py
    └── helpers.py
```

## Usage Examples

### Import the Package
```python
import quant_trader as qt

# Use indicators
rsi_values = qt.indicators.rsi(data, period=14)
sma_values = qt.indicators.sma(data, period=20)

# Use portfolio management
portfolio = qt.portfolio.Portfolio(initial_capital=100000)
optimized_weights = qt.portfolio.optimize_portfolio(returns)

# Use risk management
risk_manager = qt.risk.RiskManager(max_position_size=0.02)
position_size = risk_manager.calculate_position_size(capital, entry_price, stop_loss)

# Calculate Greeks
from quant_trader.utils import greeks
all_greeks = greeks.calculate_all_greeks(S=100, K=105, T=0.25, r=0.05, sigma=0.2)
```

## Dependencies

### Core Dependencies
- numpy >= 1.24.0
- pandas >= 2.0.0
- scipy >= 1.10.0
- matplotlib >= 3.7.0
- scikit-learn >= 1.3.0

### Reinforcement Learning
- stable-baselines3 >= 2.0.0
- gymnasium >= 0.29.0
- torch >= 2.0.0

### Options Trading
- py_vollib >= 1.0.1
- QuantLib >= 1.30 (optional, requires C++ compiler)

### Broker Integration
- ib_insync >= 0.9.86 (for Interactive Brokers)
- alpaca-py >= 0.14.0 (for Alpaca)

### Visualization
- plotly >= 5.14.0
- seaborn >= 0.12.0
- streamlit >= 1.25.0 (for dashboard)

## Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black quant_trader/

# Type checking
mypy quant_trader/

# Linting
flake8 quant_trader/
```

## Troubleshooting

### PyTorch Installation
If PyTorch installation fails, visit https://pytorch.org/ and use the appropriate command for your system.

### QuantLib Installation
QuantLib requires a C++ compiler. On macOS:
```bash
brew install boost
pip install QuantLib
```

### Interactive Brokers
To use IBKR integration:
1. Install Trader Workstation (TWS) or IB Gateway
2. Enable API connections in TWS settings
3. Install ib_insync: `pip install ib_insync`

## Verification

Test your installation:
```python
import quant_trader as qt
print(qt.__version__)  # Should print: 0.1.0

# Test indicators
import numpy as np
data = np.random.randn(100)
rsi = qt.indicators.rsi(data)
print("RSI calculated successfully!")
```

## Next Steps

1. Review the documentation in the markdown files
2. Check out example notebooks (coming soon)
3. Start with simple strategies before RL agents
4. Join discussions on GitHub Issues

## Support

For issues and questions:
- GitHub Issues: https://github.com/ravanso/Trading/issues
- Documentation: See markdown files in the repository

