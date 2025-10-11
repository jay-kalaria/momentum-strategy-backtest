import pandas as pd
from core.helper import on_or_before_date, cal_start_end, get_stock_price, fetch_data

ben_data= pd.read_pickle('cached_data/benchmark_data.pkl')

def walk_forward(tickers,benchmark_ticker, start_invest, end_invest, lookback_months, skip_months, start_capital, stop_loss):
  
  # Fetch the data
  df, not_found = fetch_data(tickers, start_invest, end_invest, lookback_months, skip_months)

  ben_data, not_found_ben = fetch_data(benchmark_ticker, start_invest, end_invest, lookback_months, skip_months)
  
  # Convert the start and end dates to datetime
  start_invest = pd.to_datetime(start_invest) 
  end_invest = pd.to_datetime(end_invest)
  lookback_months= lookback_months
  skip_months = skip_months
  top_k = 2 
  trade_records= []
  capital=start_capital
  ben_capital = start_capital
  str_mon_returns = [] 
  ben_mon_returns= [] 
  portfolio_value = []
  benchmark_value =[] 
  peak_capital = start_capital
  max_drawdown = 0
  peak_capital_ben = start_capital
  max_drawdown_ben =0 
  total_trades=0
  wins= 0

  while start_invest<=end_invest: 

    # Buy at the end of the month
    _, buy_date = on_or_before_date((start_invest + pd.offsets.MonthEnd(0)), df)

    if buy_date>end_invest:
      break

    # Sell at the end of the next month
    _, sell_date = on_or_before_date((buy_date + pd.offsets.MonthBegin(1) + pd.offsets.MonthEnd(0)), df)
    start_period, end_period = cal_start_end(buy_date, skip_months, lookback_months)
    
    # Start-End price and max diff
    start_price, start_date = on_or_before_date(start_period, df)
    end_price, end_date = on_or_before_date(end_period, df)
    diffs = (end_price-start_price).round(2)
    leaders = diffs.nlargest(top_k)
    
    # Equal weights
    w_each = 1/top_k
    capital_before = capital
    portfolio_return=0

    # Top-k leaders return
    for ticker in leaders.index:
      buy_price = get_stock_price(buy_date, ticker, df)
      sell_price = get_stock_price(sell_date, ticker, df)
      r = (sell_price-buy_price)/buy_price

      if r < (-stop_loss / 100):
        r = -stop_loss / 100
        sell_price = buy_price * (1 - stop_loss / 100)

      portfolio_return += w_each*r

      # Count trades and wins
      total_trades += 1
      if r >= 0:
        wins += 1

      trade_records.append({ 
        "buy_date": buy_date.date(),
        "sell_date": sell_date.date(),
        "window_start": start_date.date() ,
        "window_end" : end_date.date(),
        "ticker" : ticker,
        "start price": start_price[ticker],
        "end_price": end_price[ticker],
        "buy_price": buy_price,
        "sell_price":sell_price,
        "return":r 
      })
   
    #Update the capital
    capital *= (1+portfolio_return)

    print(ben_data)
    # benchmark capital
    ben_capital_before = ben_capital
    ben_return = (ben_data.loc[sell_date,benchmark_ticker] - ben_data.loc[buy_date,benchmark_ticker])/ben_data.loc[buy_date,benchmark_ticker]
    ben_capital *= 1+ ben_return
    #ben_returns.append(round(ben_capital,2))  

    # Append monthly returns
    str_mon_returns.append(portfolio_return)
    ben_mon_returns.append(ben_return)

    # Summary return
    trade_records.append({
        "buy_date": "SUMMARY" ,
        "sell_date": "SUMMARY",
        "window_start": "SUMMARY" ,
        "window_end" : "SUMMARY",
        "ticker" : "SUMMARY",
        "start price": "SUMMARY",
        "end_price": "SUMMARY",
        "buy_price": "SUMMARY",
        "sell_price": "SUMMARY", 
        "return": portfolio_return ,
        "capital_before":round(capital_before,2),
        "capital_after": round(capital,2),
        "ben_capital_before": round(ben_capital_before,2),
        "ben_capital_after": round(ben_capital,2)
      })

    benchmark_value.append(ben_capital)
    portfolio_value.append(capital)

    # Max drawdown
    if capital > peak_capital:
      peak_capital = capital
    
    # Calculate current drawdown as percentage from peak
    current_drawdown = (peak_capital - capital) / peak_capital
    max_drawdown = max(max_drawdown, current_drawdown)

    # Drawdown benchmark
    if ben_capital>peak_capital_ben:
      peak_capital_ben=ben_capital
    
    current_dd_ben = (peak_capital_ben-capital)/peak_capital_ben
    max_drawdown_ben  = max(max_drawdown_ben, current_dd_ben)

    #Date update for loop
    start_invest = (buy_date + pd.DateOffset(months=1)).replace(day=1)

  return trade_records, capital, ben_capital, str_mon_returns, ben_mon_returns, portfolio_value, benchmark_value, max_drawdown, max_drawdown_ben, total_trades, wins, not_found, not_found_ben


