
from tracemalloc import start
import pandas as pd
import numpy as np
from datetime import date


df=pd.read_pickle("cached_data/all_data.pkl")
anchor_today = pd.to_datetime('2024-12-07')
times = 3


# Calculate the start and end date
def cal_start_end(anchor, skip_months, lookback):
  end_date = (anchor-pd.DateOffset(months=skip_months+1))+ pd.offsets.MonthEnd(0)
  start_date = (anchor-pd.DateOffset(months=lookback+1+skip_months))+pd.offsets.MonthEnd(0)

  return start_date, end_date

# the prev available date
def on_or_before_date(date, col=None):
  
  if date in df.index:
    val = df.loc[date, col] if col is not None else df.loc[date]
    prev_date =date

  else:  
    pos = df.index.searchsorted(date, side='right')-1
    if pos<0:
      raise ValueError("No available date on/before the given date")
    prev_date = df.index[pos]
    val= df.loc[prev_date, col] if col is not None else df.loc[prev_date]


  return val, prev_date


# Get Stock Price
def get_stock_price(date, ticker):
  return df.loc[date,ticker]

# Calculate CAGR
def calc_cagr(start_cap, end_cap, returns, start_date, end_date):

  years= (end_date-start_date).days/265.25

  if years<=0 or start_cap<=0 :
    return np.nan

  return (end_cap/start_cap)**(1/years)-1
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



#Calculate Sharpe
def calc_sharpe(returns, annual_rf):

  r = pd.Series(returns).dropna()
  if len(r)<2:
    return np.nan

  rf_monthly = (1+annual_rf)**(1/12)-1

  excess_returns = r - rf_monthly  
  mean_excess = excess_returns.mean()
  std_excess = excess_returns.std(ddof=1)

  if std_excess==0 or np.isnan(std_excess):
    return np.nan

  sharpe = (mean_excess/std_excess)* np.sqrt(12)
  return sharpe






