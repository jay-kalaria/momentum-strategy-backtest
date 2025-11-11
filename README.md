# Momentum Market Strategy Backtester

A momentum-based trading strategy backtesting system that selects top-performing stocks based on historical price momentum and evaluates performance against market benchmarks.
<img width="1510" height="815" alt="Pasted Graphic 2" src="https://github.com/user-attachments/assets/e0d40f1f-1034-4fbd-9165-3c5d3d447a0e" />

## What It Does

This tool implements a **time-series momentum strategy** that:

1. **Analyzes Historical Performance**: Looks back over a specified period (1-24 months) to identify stocks with strong momentum
2. **Selects Top Performers**: Chooses the top N stocks based on price appreciation during the lookback period
3. **Builds Portfolio**: Creates an equally-weighted portfolio of selected stocks
4. **Manages Risk**: Implements stop-loss protection to limit downside risk
5. **Rebalances Monthly**: Updates portfolio holdings each month based on updated momentum signals
6. **Compares to Benchmark**: Evaluates strategy performance against market benchmarks (e.g., S&P 500)

## Analysis & Metrics

The backtester provides comprehensive performance analysis across multiple dimensions:

### Return Metrics

-   **Total Return**
-   **CAGR (Compound Annual Growth Rate)**
-   **Monthly Returns**

### Risk-Adjusted Metrics

-   **Sharpe Ratio**
-   **Sortino Ratio**
-   **Volatility**
-   **Maximum Drawdown**

### Trading Performance Metrics

-   **Win Rate**
-   **Total Trades**

### Benchmark Comparison

All metrics are calculated for both the strategy and benchmark, allowing direct comparison to assess whether the strategy adds value over passive market exposure.

### Visualizations

-   **Portfolio Value Chart**
-   **Trade Records**

## Setup

### Prerequisites

-   Python 3.7+
-   pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jay-kalaria/momentum-strategy-backtest
cd momentum-market
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

## Usage

1. **Configure Parameters** in the sidebar:

    - **Tickers**: Comma-separated stock symbols (e.g., `AAPL,MSFT,AMZN`)
    - **Benchmark**: Benchmark ticker (e.g., `SPY`)
    - **Time Period**: Start and end dates for backtesting
    - **Lookback Months**: Historical period for momentum calculation (1-24 months)
    - **Skip Months**: Gap between lookback period and investment (0-6 months)
    - **Top N Stocks**: Number of stocks to select for portfolio
    - **Stop Loss**: Maximum loss percentage per trade (0-50%)

2. **Run Strategy**: Click "Run Strategy" to execute the backtest

3. **Review Results**: View performance metrics, charts, and trade records in the results tab

## Strategy Parameters

| Parameter         | Description                                | Range | Default |
| ----------------- | ------------------------------------------ | ----- | ------- |
| `lookback_months` | Historical period for momentum calculation | 1-24  | 6       |
| `skip_months`     | Gap between analysis and investment        | 0-6   | 1       |
| `top_n`           | Number of stocks to select                 | 1+    | 3       |
| `stop_loss`       | Maximum loss per trade (%)                 | 0-50  | 50      |

---

**Note**: This is a backtesting framework for research and educational purposes. Not intended for live trading without proper testing and risk management.
