import pandas as pd


df=pd.read_pickle("cached_data/all_data.pkl")
anchor_today = pd.to_datetime('2024-12-07')
times = 3


# Calculate the start and end date
def cal_start_end(anchor, skip_months, lookback):
  end_date = (anchor-pd.DateOffset(months=skip_months+1))+ pd.offsets.MonthEnd(0)
  start_date = (anchor-pd.DateOffset(months=lookback+1+skip_months))+pd.offsets.MonthEnd(0)

  return start_date, end_date

# the prev available date
def on_or_before(date, col=None):
  if date in df.index:
    val = df.loc[date, col] if col is not None else df.loc[date]
    prev_date =date

  else:  
    pos = df.index.searchsorted(date, side='left')-1
    if pos<0:
      raise ValueError("No available date on/before the given date")
    prev_date = df.index[pos]
    val= df.loc[prev_date, col] if col is not None else df.loc[prev_date]

  return val, prev_date

# the next available date
def on_or_after(date , col=None):
  
  pos= df.index.searchsorted(date, side='left')
  if pos<0:
      raise ValueError("No available date on/before the given date")
  next_date = df.index[pos]

  val= df.loc[next_date,col] if col is not None else df.loc[next_date]

  return val, next_date
