# Trading Strategies

## Purpose
Document all trading strategy ideas, their logic, parameters, and expected behavior.

---

## Strategy Template

### Strategy Name: [Name]

**Type:** (Trend Following, Mean Reversion, Momentum, Arbitrage, etc.)

**Timeframe:** (1min, 5min, 1H, Daily, etc.)

**Markets:** (Stocks, Crypto, Forex, etc.)

**Description:**
Brief overview of the strategy logic.

**Entry Conditions:**
1. 
2. 
3. 

**Exit Conditions:**
1. Stop Loss:
2. Take Profit:
3. Time-based:

**Position Sizing:**
- Fixed size, volatility-based, Kelly criterion, etc.

**Risk/Reward:**
- Target R:R ratio
- Win rate expectations

**Indicators/Tools:**
- Technical indicators
- Fundamental data
- Alternative data

**Backtesting Notes:**
- Historical performance expectations
- Market conditions where it works best
- Known limitations

**Implementation Priority:**
- High / Medium / Low

---

## AI Agent Training Approach

### Reinforcement Learning Framework
The AI agent will learn through reinforcement learning, where it:
1. Observes market state (prices, Greeks, IV, volume, etc.)
2. Takes action (enter trade, exit trade, hold, adjust position)
3. Receives reward (P&L, risk-adjusted returns)
4. Learns optimal policy over time

### State Space (What the agent sees)
- Current stock price and price history
- Options chain data (strikes, expiries, bid/ask, volume, OI)
- Greeks (Delta, Gamma, Theta, Vega, Rho)
- Implied Volatility (IV) and IV Rank
- Technical indicators (RSI, Moving Averages, etc.)
- Market conditions (VIX, trend, volatility regime)
- Current portfolio state (positions, P&L, Greeks exposure)

### Action Space (What the agent can do)
- Enter new position (specify strategy, strikes, expiry)
- Close existing position
- Adjust position (roll, add legs, etc.)
- Hold/do nothing

### Reward Function
Design reward to optimize for:
- Profit (weighted by time)
- Risk-adjusted returns (Sharpe ratio)
- Drawdown minimization
- Consistency of returns

---

## Options Strategies for the Agent

### Strategy 1: Vertical Credit Spreads
**Type:** Premium Selling, Defined Risk

**Timeframe:** 30-45 DTE (Days to Expiration)

**Markets:** SPX, SPY, QQQ, liquid stocks

**Description:**
Sell vertical spreads (bull put spreads or bear call spreads) with high probability of profit. Target 0.20-0.30 delta short strikes in low IV environments.

**Entry Conditions:**
1. IV Rank < 50 (prefer directional bias over volatility)
2. Clear support/resistance levels
3. Trend confirmation (moving averages, momentum)
4. Risk/Reward ratio >= 1:2 (credit received vs max loss)
5. Sufficient liquidity (tight bid/ask spreads)

**Exit Conditions:**
1. Stop Loss: Close at 2x credit received
2. Take Profit: Close at 50-75% of max profit
3. Time-based: Close at 21 DTE or 7-10 days before expiry
4. Technical: Exit if support/resistance breaks

**Position Sizing:**
- Risk 1-2% of account per trade
- Maximum 5-10 positions open simultaneously
- Diversify across different underlyings

**Risk/Reward:**
- Target win rate: 65-75%
- Target R:R: 1:2 to 1:3

**Indicators/Tools:**
- Support/Resistance levels
- Moving averages (20, 50, 200 SMA)
- RSI for overbought/oversold
- IV Rank/Percentile
- Volume profile

**Agent Learning Goals:**
- Optimal strike selection
- Best entry timing
- When to take profits vs let expire
- Position adjustment decisions

**Implementation Priority:** High

---

### Strategy 2: Iron Condors
**Type:** Neutral/Range-bound, Premium Selling

**Timeframe:** 30-45 DTE

**Markets:** SPX, SPY, RUT (high liquidity, big indexes)

**Description:**
Sell both a call spread and put spread to profit from low volatility and range-bound markets. Collect premium from both sides while price stays within range.

**Entry Conditions:**
1. IV Rank > 50 (high premium environment)
2. Low directional bias / sideways market
3. Price in consolidation range
4. Sell 0.16 delta on both sides (approx 1 standard deviation)
5. Credit received >= 25% of spread width

**Exit Conditions:**
1. Stop Loss: Close entire position at 2x credit received
2. Take Profit: Close at 50% of max profit
3. Time-based: Manage at 21 DTE
4. Adjustment: Roll untested side or convert to vertical if tested

**Position Sizing:**
- Risk 2-3% per trade
- Maintain balanced portfolio (not too many correlated positions)

**Risk/Reward:**
- Target win rate: 60-70%
- Target monthly return: 5-10% on capital deployed

**Indicators/Tools:**
- Bollinger Bands (range identification)
- ATR (volatility measurement)
- VIX (market fear gauge)
- Expected move calculations

**Agent Learning Goals:**
- Identify optimal range-bound conditions
- Learn when to adjust vs close
- Width of strikes selection
- Portfolio-level Greeks management

**Implementation Priority:** High

---

### Strategy 3: Volatility Trading (Straddles/Strangles)
**Type:** Volatility Play, Non-directional

**Timeframe:** Pre-earnings or event-driven (1-7 DTE)

**Markets:** High IV stocks before earnings/events

**Description:**
Buy or sell straddles/strangles based on IV expectations vs actual volatility. Profit from IV crush (selling) or large moves (buying).

**Entry Conditions (Selling IV):**
1. IV Rank > 70 (very high premium)
2. Upcoming catalyst (earnings, FDA approval, etc.)
3. Historical IV crush pattern
4. Sufficient premium to justify risk

**Entry Conditions (Buying):**
1. IV low relative to expected move
2. Anticipating volatility expansion
3. Major catalyst expected

**Exit Conditions:**
1. IV Sellers: Exit immediately after event (IV crush)
2. IV Buyers: Exit on volatility spike or time decay threshold
3. Stop loss based on max loss tolerance

**Position Sizing:**
- More conservative: 1-2% risk (volatility can spike quickly)

**Agent Learning Goals:**
- Predict IV crush magnitude
- Identify mispriced volatility
- Event-specific patterns
- Timing of entry/exit around catalysts

**Implementation Priority:** Medium

---

### Strategy 4: Trend Following with LEAPS
**Type:** Directional, Long-term

**Timeframe:** 90-365+ DTE

**Markets:** Strong trending stocks/ETFs

**Description:**
Buy deep ITM or ATM LEAPS (Long-term Equity Anticipation Securities) to gain leveraged exposure to strong trends with defined risk.

**Entry Conditions:**
1. Strong established trend (moving average alignment)
2. Momentum confirmation
3. Buy 0.60-0.80 delta options (acts like stock)
4. Good liquidity in long-dated options

**Exit Conditions:**
1. Stop Loss: Technical breakdown or 20-30% loss
2. Take Profit: Target hit or trend breaks
3. Trail stop based on ATR

**Position Sizing:**
- 2-5% risk per position
- Leverage allows diversification across multiple positions

**Agent Learning Goals:**
- Identify sustainable trends
- Optimal entry points (pullbacks vs breakouts)
- When to add to winners
- Dynamic position sizing

**Implementation Priority:** Medium

---

### Strategy 5: Delta-Neutral Portfolio
**Type:** Market-neutral, Greeks arbitrage

**Timeframe:** Variable

**Markets:** Options + underlying stock/ETF

**Description:**
Maintain delta-neutral portfolio to profit from theta decay, gamma scalping, or vega changes while minimizing directional risk.

**Entry Conditions:**
1. Construct multi-leg positions
2. Balance Greeks (Delta near 0)
3. Positive theta preferred

**Exit Conditions:**
1. Rebalance when delta drifts beyond threshold
2. Close when Greeks profile deteriorates
3. Take profits on volatility expansion

**Agent Learning Goals:**
- Dynamic Greeks hedging
- Optimal rebalancing frequency
- Portfolio-level risk management
- Greeks arbitrage opportunities

**Implementation Priority:** Low (Advanced)




---

## Strategy Research

### Concepts to Explore
- 
- 
- 

### Papers and Resources
- 

---

## Notes
- Keep strategies simple and testable
- Focus on robust strategies that work across market conditions
- Document assumptions clearly

