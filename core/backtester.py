import pandas as pd
from core.helper import on_or_before_date, cal_start_end, get_stock_price

ben_data= pd.read_pickle('cached_data/benchmark_data.pkl')

def walk_forward(start_invest, end_invest, lookback_months, skip_months, start_capital):
  
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

  while start_invest<=end_invest: 

    # Buy at the end of the month
    _, buy_date = on_or_before_date((start_invest + pd.offsets.MonthEnd(0)))
    # Sell at the end of the next month
    _, sell_date = on_or_before_date((buy_date + pd.offsets.MonthBegin(1) + pd.offsets.MonthEnd(0)))
    start_period, end_period = cal_start_end(buy_date, skip_months, lookback_months)
    
    # Start-End price and max diff
    start_price, start_date = on_or_before_date(start_period)
    end_price, end_date = on_or_before_date(end_period)
    diffs = (end_price-start_price).round(2)
    leaders = diffs.nlargest(top_k)
    
    # Equal weights
    w_each = 1/top_k
    capital_before = capital
    portfolio_return=0

    # Top-k leaders return
    for ticker in leaders.index:
      buy_price = get_stock_price(buy_date, ticker)
      sell_price = get_stock_price(sell_date, ticker)
      r = (sell_price-buy_price)/buy_price
      portfolio_return += w_each*r

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

    # benchmark capital
    ben_capital_before = ben_capital
    ben_return = (ben_data.loc[sell_date,"S&P 500"] - ben_data.loc[buy_date,"S&P 500"])/ben_data.loc[buy_date,"S&P 500"]
    ben_capital *= 1+ ben_return
    #ben_returns.append(round(ben_capital,2))  

    # Append monthly returns
    str_mon_returns.append(portfolio_return)
    ben_mon_returns.append(ben_return)

    # Summary return
    trade_records.append({
        "invest_date": "SUMMARY" ,
        "sell_date": "SUMMARY",
        "window_start": "SUMMARY" ,
        "window_end" : "SUMMARY",
        "ticker" : "SUMMARY",
        "start price": "SUMMARY",
        "end_price": "SUMMARY",
        "invest_price": "SUMMARY",
        "sell_price": "SUMMARY", 
        "return": portfolio_return ,
        "capital_before":round(capital_before,2),
        "capital_after": round(capital,2),
        "ben Capital before": round(ben_capital_before,2),
        "ben_capital_after": round(ben_capital,2)
      })

    benchmark_value.append(ben_capital)
    portfolio_value.append(capital)


    print(start_invest)
    start_invest = (buy_date + pd.DateOffset(months=1)).replace(day=1)

    

  return trade_records, capital, ben_capital, str_mon_returns, ben_mon_returns, portfolio_value, benchmark_value