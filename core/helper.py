from curses import raw
from tracemalloc import start
from pandas import DataFrame
import numpy as np
from datetime import date
import yfinance as yf
import pandas as pd


# df=pd.read_pickle("cached_data/all_data.pkl")
anchor_today = pd.to_datetime("2024-12-07")
times = 3


def fetch_data(tickers, start_invest, end_invest, look_back, skip_months):

    tickers = [
        ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()
    ]


    start_offset_months = look_back + 2 + skip_months + 60 
    start_invest = pd.to_datetime(start_invest) - pd.DateOffset(
        months=start_offset_months
    )

    end_invest = pd.to_datetime(end_invest)
    max_possible_date = pd.to_datetime("today")
    proposed_end = end_invest + pd.DateOffset(months=2)
    if proposed_end < max_possible_date:
        end_invest = proposed_end
    else:
        end_invest = max_possible_date

    raw_data = yf.download(
        tickers=tickers,
        start=start_invest,
        end=end_invest,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
    )

    adj_close_dict = {}

    not_found = []

    for ticker in tickers:
      if hasattr(raw_data.columns, "levels"):
        ticker_data = raw_data[ticker]["Adj Close"]
        
        if ticker_data.isna().all():
          not_found.append(ticker)
          continue
        else:
          adj_close_dict[ticker] = ticker_data

      else:
          ticker_data = raw_data[ticker]
          if ticker_data.isna().all():
            not_found.append(ticker)
            continue
          else:
            adj_close_dict[ticker] = ticker_data
          

    data = pd.DataFrame(adj_close_dict)

    final_data = data.ffill().bfill().round(2)
    

    return final_data, not_found


# Calculate the start and end date
def cal_start_end(anchor, skip_months, lookback):
    end_date = (anchor - pd.DateOffset(months=skip_months + 1)) + pd.offsets.MonthEnd(0)
    start_date = (
        anchor - pd.DateOffset(months=lookback + 1 + skip_months)
    ) + pd.offsets.MonthEnd(0)

    return start_date, end_date


# the prev available date
def on_or_before_date(date, df, col=None):

    if date in df.index:
        val = df.loc[date, col] if col is not None else df.loc[date]
        prev_date = date

    else:
        pos = df.index.searchsorted(date, side="right") - 1
        if pos < 0:
            raise ValueError("No available date on/before the given date")
        prev_date = df.index[pos]
        val = df.loc[prev_date, col] if col is not None else df.loc[prev_date]

    return val, prev_date


# Get Stock Price
def get_stock_price(date, ticker, df):
    return df.loc[date, ticker]


# Calculate CAGR
def calc_cagr(start_cap, end_cap, returns, start_date, end_date):

    years = (end_date - start_date).days / 365.25

    if years <= 0 or start_cap <= 0:
        return np.nan

    # Calculate CAGR
    cagr = (end_cap / start_cap) ** (1 / years) - 1

    return cagr
    # Log errors as well

    # if not start_cap or not end_cap or len(returns)==0:
    #   return np.nan

    # r = pd.Series(returns).dropna()
    # n_len = len(r)
    # growth = (1+r).prod() # (1+r) same as the ratio end/start

    # print("============")
    # print(end_cap/start_cap)
    # print(growth)
    # print("============")

    # #second_way = (end_cap/start_cap)**(12/n_len)-1

    # return growth**(12/n_len)-1


# Calculate Sharpe Ratio
def calc_sharpe(returns, annual_rf):
    r = pd.Series(returns).dropna()

    if len(r) < 2:
        return np.nan

    # Convert annual risk-free rate to monthly
    rf_monthly = (1 + annual_rf) ** (1 / 12) - 1

    # Calculate excess returns
    excess_returns = r - rf_monthly

    # Calculate mean and standard deviation of excess returns
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std(ddof=1)

    if std_excess == 0 or np.isnan(std_excess):
        return np.nan

    # Calculate Sharpe ratio
    sharpe = (mean_excess / std_excess) * np.sqrt(12)

    return sharpe


def calc_volatility(returns):

    r = pd.Series(returns).dropna()

    if len(r) < 2:
        return np.nan

    monthly_vol = r.std(ddof=1)
    annual_vol = monthly_vol * np.sqrt(12)

    return annual_vol


# Calculate Sortino Ratio
def calc_sortino(returns, annual_rf, target_return=0):

    r = pd.Series(returns).dropna()

    if len(r) < 2:
        return np.nan

    # Convert annual risk-free rate to monthly
    rf_monthly = (1 + annual_rf) ** (1 / 12) - 1

    # Calculate excess returns
    excess_returns = r - rf_monthly

    downside_returns = excess_returns[excess_returns < target_return]

    if len(downside_returns) < 2:
        return np.nan

    # Calculate downside deviation annualized
    downside_deviation = downside_returns.std(ddof=1) * np.sqrt(12)

    if downside_deviation == 0 or np.isnan(downside_deviation):
        return np.nan

    mean_excess_return = excess_returns.mean() * 12  # Annualized
    sortino = mean_excess_return / downside_deviation

    return sortino


if __name__ == "__main__":
    tickers = ["AAPL"]
    start_invest = "2022-01-01"
    end_invest = "2023-01-01"
    lookback_months = 6
    skip_months = 1

    data = fetch_data(tickers, start_invest, end_invest)
    print("Sample data:")
    print(data.head())
    print(f"\nData shape: {data.shape}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
