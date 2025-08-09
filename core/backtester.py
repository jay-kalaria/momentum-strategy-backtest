import pandas as pd
from core.helper import on_or_before, on_or_after, cal_start_end



def walk_forward(start_invest, end_invest, lookback_months, skip_months, start_capital):

  start_invest = pd.to_datetime(start_invest) 
  end_invest = pd.to_datetime(end_invest)
  buy_date = start_invest
  lookback_months= lookback_months
  skip_months = skip_months
  top_k =2 
  trade_records= []
  capital=start_capital

  while buy_date<=end_invest: 

    # Cal period
    buy_date = buy_date.replace(day=1)  
    sell_date = buy_date + pd.offsets.MonthEnd(0)
    start_period, end_period = cal_start_end(buy_date, skip_months, lookback_months)
    
    # Start-End price and max diff
    start_price, start_date = on_or_before(start_period)
    end_price, end_date = on_or_before(end_period)
    diffs = (end_price-start_price).round(2)
    leaders = diffs.nlargest(top_k)
    
    print(buy_date, sell_date)
    w_each = 1/top_k
    capital_before = capital
    portfolio_return=0

    for ticker in leaders.index:
      invest_price, invest_date = on_or_after(buy_date,ticker)
      sell_price, sell_date = on_or_before(sell_date,ticker)
      r = (sell_price-invest_price)/invest_price  
      portfolio_return += w_each*r

      trade_records.append({ 
        "invest_date": invest_date.date(),
        "sell_date": sell_date.date(),
        "window_start": start_date.date() ,
        "window_end" : end_date.date(),
        "ticker" : ticker,
        "start price": start_price[ticker],
        "end_price": end_price[ticker],
        "invest_price": invest_price,
        "sell_price":sell_price,
        "return":r 
      })

    capital *= (1+portfolio_return)

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
        "capital_after": round(capital,2)
      })

    buy_date = (buy_date + pd.DateOffset(months=1)).replace(day=1)

  return trade_records