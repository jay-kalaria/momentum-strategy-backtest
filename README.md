# Momentum Market Strategy Backtester

A comprehensive momentum-based trading strategy backtesting system with optimization capabilities, built with Streamlit and powered by Optuna for hyperparameter optimization.

## 🚀 Features

-   **Momentum Strategy Implementation**: Implements a time-series momentum strategy that selects top-performing stocks based on historical performance
-   **Interactive Web Interface**: User-friendly Streamlit dashboard for strategy configuration and results visualization
-   **Comprehensive Backtesting**: Walk-forward analysis with detailed performance metrics
-   **Hyperparameter Optimization**: Automated parameter tuning using Optuna for optimal strategy performance
-   **Risk Management**: Built-in stop-loss functionality and risk-adjusted performance metrics
-   **Benchmark Comparison**: Compare strategy performance against market benchmarks (e.g., S&P 500)

## 📊 Strategy Overview

The momentum strategy works as follows:

1. **Lookback Period**: Analyzes stock performance over a specified lookback period (1-24 months)
2. **Skip Period**: Skips a specified number of months between the lookback period and investment decision
3. **Stock Selection**: Selects the top N performing stocks based on price momentum
4. **Portfolio Construction**: Creates an equally-weighted portfolio of selected stocks
5. **Risk Management**: Implements stop-loss protection to limit downside risk
6. **Rebalancing**: Rebalances the portfolio monthly based on updated momentum signals

## 🛠️ Installation

### Prerequisites

-   Python 3.7+
-   pip package manager

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd momentum-market
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

## 📁 Project Structure

```
momentum-market/
├── app.py                 # Main Streamlit application
├── core/
│   ├── backtester.py     # Core backtesting engine
│   └── helper.py         # Utility functions and calculations
├── optimizer.ipynb       # Optuna optimization notebook
├── algo.ipynb           # Algorithm development notebook
├── test.ipynb           # Testing and validation notebook
├── us100.py             # US100 stock universe definition
├── cached_data/         # Cached market data
│   ├── all_data.pkl
│   └── benchmark_data.pkl
└── requirements.txt     # Python dependencies
```

## 🎯 Usage

### Web Interface

1. Launch the application:

```bash
streamlit run app.py
```

2. Configure strategy parameters in the sidebar:

    - **Tickers**: Enter comma-separated stock symbols
    - **Benchmark**: Specify benchmark ticker (e.g., SPY)
    - **Time Period**: Set start and end dates
    - **Lookback Months**: Historical period for momentum calculation
    - **Skip Months**: Gap between lookback and investment
    - **Top N Stocks**: Number of stocks to select
    - **Stop Loss**: Maximum loss percentage per trade

3. Click "Run Strategy" to execute the backtest

4. View results across three tabs:
    - **Results and Comparison**: Performance metrics and charts
    - **Monthly Performance**: Detailed trade records
    - **Detailed Analysis**: Comprehensive risk and return analysis

### Optimization

Use the Jupyter notebook for hyperparameter optimization:

```python
# Open optimizer.ipynb
# Configure optimization parameters
# Run optimization trials
```

## 📈 Performance Metrics

The system calculates comprehensive performance metrics:

### Return Metrics

-   **Total Return**: Overall portfolio performance
-   **CAGR**: Compound Annual Growth Rate
-   **Monthly Returns**: Time series of monthly returns

### Risk Metrics

-   **Sharpe Ratio**: Risk-adjusted returns
-   **Sortino Ratio**: Downside risk-adjusted returns
-   **Volatility**: Annualized return volatility
-   **Maximum Drawdown**: Largest peak-to-trough decline

### Trading Metrics

-   **Win Rate**: Percentage of profitable trades
-   **Total Trades**: Number of executed trades
-   **Trade Records**: Detailed transaction history

## 🔧 Configuration

### Strategy Parameters

| Parameter         | Description                         | Range | Default |
| ----------------- | ----------------------------------- | ----- | ------- |
| `lookback_months` | Historical analysis period          | 1-24  | 6       |
| `skip_months`     | Gap between analysis and investment | 0-6   | 1       |
| `top_n`           | Number of stocks to select          | 1-10  | 2       |
| `stop_loss`       | Maximum loss per trade (%)          | 0-50  | 50      |

### Data Sources

-   **Market Data**: Yahoo Finance (via yfinance)
-   **Stock Universe**: Configurable ticker lists
-   **Benchmarks**: Any valid ticker symbol

## 🧪 Optimization

The system includes Optuna-based hyperparameter optimization:

```python
# Example optimization objective
def objective(trial):
    lookback_months = trial.suggest_int("lookback_months", 1, 12)
    skip_months = trial.suggest_int("skip_months", 0, 6)
    stop_loss = trial.suggest_float("stop_loss", 0, 0.5)

    # Run backtest and return performance score
    return performance_score
```

## 📊 Example Results

The system provides comprehensive performance analysis including:

-   Portfolio value progression charts
-   Benchmark comparison
-   Risk-adjusted performance metrics
-   Trade-by-trade analysis
-   Drawdown analysis

## 🔍 Technical Details

### Data Handling

-   **Data Source**: Yahoo Finance API
-   **Data Processing**: Forward-fill missing values
-   **Caching**: Optional data caching for faster repeated runs

### Backtesting Engine

-   **Method**: Walk-forward analysis
-   **Rebalancing**: Monthly portfolio rebalancing
-   **Transaction Costs**: Not included (can be added)
-   **Slippage**: Not modeled

### Risk Management

-   **Stop Loss**: Configurable percentage-based stop loss
-   **Position Sizing**: Equal-weight portfolio construction
-   **Rebalancing**: Monthly rebalancing based on momentum signals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🆘 Support

For questions, issues, or contributions, please open an issue on the GitHub repository.

---

**Note**: This is a backtesting framework and should not be used for live trading without proper testing and risk management procedures.

