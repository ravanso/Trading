# Data Sources and APIs

## Purpose
Document all potential data sources, APIs, and data requirements for the trading system.

---

## Data Requirements

### Market Data Needs
- [ ] Real-time quotes
- [ ] Historical OHLCV data
- [ ] Level 2 / Order book data
- [ ] Tick data
- [ ] Volume profile
- [ ] Corporate actions (splits, dividends)

### Options-Specific Data (Critical for this project)
- [ ] Full options chains (all strikes, all expirations)
- [ ] Real-time options quotes (bid/ask/last)
- [ ] Historical options prices
- [ ] Greeks (Delta, Gamma, Theta, Vega, Rho)
- [ ] Implied Volatility (IV) for each option
- [ ] Open Interest (OI) and volume by strike
- [ ] IV Rank and IV Percentile
- [ ] Historical volatility (HV)
- [ ] Options trade flow data
- [ ] Earnings calendar and events
- [ ] Expected move calculations

### Fundamental Data
- [ ] Financial statements
- [ ] Earnings reports
- [ ] Economic indicators
- [ ] News and sentiment

### Alternative Data
- [ ] Social media sentiment
- [ ] Web scraping
- [ ] Satellite imagery
- [ ] Other sources

---

## Data Providers

### Free/Open Source

#### Provider 1: Yahoo Finance (yfinance)
**Data Available:**
- Historical OHLCV for stocks
- Basic options chains (current)
- Limited historical options data

**API/Library:**
- yfinance (Python)

**Limitations:**
- Rate limits
- Delayed data (15-20 min)
- Limited historical options data
- No Greeks calculation
- Unreliable for production

**Cost:** Free

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Notes:** Good for initial prototyping and testing, but insufficient for production trading.

---

#### Provider 2: CBOE DataShop
**Data Available:**
- End-of-day options data
- VIX data
- Historical volatility data

**API/Library:**
- Direct download, custom parsing needed

**Limitations:**
- End-of-day only (no intraday)
- Delayed by one day
- Manual data handling

**Cost:** Free (delayed data)

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Notes:** Useful for backtesting but not for live trading.

---

### Premium Providers (Options-Focused)

#### Provider 1: Interactive Brokers (IBKR)
**Data Available:**
- Real-time options chains
- Greeks (calculated)
- Historical options data
- Implied volatility
- Execution capabilities

**API/Library:**
- ib_insync (Python wrapper)
- TWS API (official)

**Limitations:**
- Requires brokerage account
- Market data subscriptions needed
- API complexity
- Rate limits on historical data requests

**Cost:**
- Account minimum: $0-10,000 (depending on account type)
- Market data: $1-4.50/month per exchange
- Commissions: ~$0.65 per options contract

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** HIGH - Best for live trading integration

---

#### Provider 2: Tradier
**Data Available:**
- Real-time options chains
- Historical options data
- Greeks
- IV and volatility metrics
- Market data streaming

**API/Library:**
- REST API
- Streaming WebSocket API
- Python SDK available

**Limitations:**
- Historical options data is limited
- Smaller market share than IBKR

**Cost:**
- Market data: Free with brokerage account or $10/month
- Commissions: $0.35 per contract (Tradier Brokerage)
- API access: Free

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** HIGH - Clean API, good for data and execution

---

#### Provider 3: Polygon.io
**Data Available:**
- Real-time and historical options data
- Options chains
- Greeks (computed)
- Trades and quotes
- Aggregates

**API/Library:**
- REST API
- WebSocket streaming
- Python client

**Limitations:**
- No execution capabilities (data only)
- Need separate broker for trading

**Cost:**
- Starter: $29/month (delayed data)
- Developer: $99/month (real-time stocks, delayed options)
- Advanced: $199/month (real-time options)
- Options data add-on: +$100/month

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** MEDIUM - Good for data, but need separate execution

---

#### Provider 4: Alpaca Markets
**Data Available:**
- Real-time and historical stock data
- Options trading (beta)
- Options chains

**API/Library:**
- REST API
- Python SDK (alpaca-py)
- WebSocket streaming

**Limitations:**
- Options support is newer/limited
- Fewer options data features than IBKR
- U.S. customers only

**Cost:**
- Paper trading: Free
- Live trading: Free (commission-free)
- Market data: Free for stocks, options in development

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** MEDIUM - Good for stocks, options still developing

---

#### Provider 5: Theta Data
**Data Available:**
- Historical options data (tick-level)
- End-of-day data
- Greeks
- Implied volatility
- 3+ years of historical data

**API/Library:**
- REST API
- Python client

**Limitations:**
- Historical data only (no live trading)
- Need separate broker for execution

**Cost:**
- Standard: $59/month (end-of-day)
- Pro: $149/month (end-of-day + snapshots)
- Enterprise: Custom pricing (tick data)

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** HIGH - Excellent for backtesting and training AI agent

---

#### Provider 6: OPRA (Options Price Reporting Authority)
**Data Available:**
- Official options market data feed
- Most comprehensive and accurate
- Real-time quotes and trades

**API/Library:**
- Requires vendor/exchange connection
- Not direct API access

**Limitations:**
- Expensive
- Complex setup
- Requires professional infrastructure

**Cost:**
- $$$$ (thousands per month)
- Enterprise-level only

**Status:** [ ] Evaluated [ ] Integrated [ ] Active

**Priority:** LOW - Too expensive for initial project

---

## Data Storage

### Storage Strategy
- Database type (PostgreSQL, TimescaleDB, InfluxDB, SQLite)
- File storage (CSV, Parquet, HDF5)
- Caching strategy
- Backup approach

### Data Schema
(To be defined)

---

## Data Pipeline

### Ingestion Process
1. Data collection
2. Validation
3. Cleaning
4. Storage
5. Update frequency

### Data Quality Checks
- Missing data handling
- Outlier detection
- Data integrity validation

---

## Notes and Considerations
- Data quality is critical for backtesting accuracy
- Consider data survivorship bias
- Plan for data storage and archival
- Implement proper error handling and logging

