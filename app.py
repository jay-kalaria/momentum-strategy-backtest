from core.helper import calc_cagr, calc_sharpe
import streamlit as st
import pandas as pd
from core.backtester import walk_forward
import datetime

st.title("Momentum Strategy Backtester with")

NAME_TO_TICKER = {
    "ApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdfApplefsfsdfdfsfsdf": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Tesla": "TSLA",
    # … add others you plan to demo
}

names = NAME_TO_TICKER.keys()

#st.write("Select parameters and see portfolio returns")
#st.multiselect("Select companies", options=names)
# with st.container(border=True):
#   st.write("S&P 500 stocks")
#   st.button("Select this")
st.write("Select parameters and see portfolio returns")
with st.sidebar:
  st.header("Parameters")

  # Stock and benchmark selection




  #Period
  start_invest = st.date_input("Starting date", value = pd.to_datetime("2022-01-01"))
  end_invest = st.date_input("Ending date", value = pd.to_datetime("2023-01-01"))
  
  # Lookback and skip input
  lookback_months= st.number_input("Lookback months", min_value=1 , max_value=24, value=6)
  skip_months = st.number_input("Skip Months", min_value=0 , max_value=6, value=1)
  start_capital = st.number_input("Start Capital", min_value=100 , value=100 )
  run = st.button("Run strategy")
  reset = st.button("Reset")



# Reset button
if reset:
  st.session_state.clear()


if run:
  
  with st.spinner("Running backtest...This may take a few moments"):
    trade_records, capital, ben_capital, str_mon_returns, ben_mon_returns, portfolio_value, benchmark_value  = walk_forward(start_invest, end_invest, lookback_months, skip_months, start_capital)

    sharpe  = calc_sharpe(str_mon_returns, 0.04)
    cagr = calc_cagr(start_capital, capital, str_mon_returns, start_invest, end_invest)




  total_returns = (((capital-start_capital)/start_capital)*100).round(2)

  
 # st.success("Backtest completed!")

  tab1,tab2,tab3 = st.tabs(["Result and Comparsion","Monthly Performace","Detailed Analysis"])

  graph_data= pd.DataFrame(
    {
      "Momentum Strategy": portfolio_value, 
      "Benchmark": benchmark_value
    }
  )


  with tab2:
    st.dataframe(trade_records)


  with tab1:
    # st.header("Results")
    # st.subheader("Results")
    # st.metric(label="Strategy Capital", value=capital)
    # st.metric(label="Benchmark Capital", value=ben_capital)
   # st.dataframe(trade_records)
    # st.metric(label="Total returns" , value = total_returns)
    # st.write(f"**Returns**: {total_returns:.2f}")
    # st.write(f"**CAGR**: {cagr:.2f}")
    # st.write(f"**Sharpe**: {sharpe:.2f}")

    st.line_chart(graph_data)

    # Performance Panel
    st.subheader("Performance Panel")
    p1, p2 = st.columns(2)
    with p1:
      st.metric("Strategy Total Return", "—")
    with p2:
      st.metric("Benchmark Total Return", "—")

    p3, p4 = st.columns(2)
    with p3:
      st.metric("Strategy CAGR", "—", delta="+5.4%")
    with p4:
      st.metric("Benchmark CAGR", "—")

    # Risk-Adjusted Panel
    st.subheader("Risk-Adjusted Panel")
    r1, r2 = st.columns(2)
    with r1:
      st.metric("Strategy Sharpe", "—")
    with r2:
      st.metric("Benchmark Sharpe", "—")

    r3, r4 = st.columns(2)
    with r3:
      st.metric("Volatility (Strategy)", "—")
    with r4:
      st.metric("Volatility (Benchmark)", "—")

    r5, r6 = st.columns(2)
    with r5:
      st.metric("Max Drawdown (Strategy)", "—")
    with r6:
      st.metric("Max Drawdown (Benchmark)", "—")

    # Extras Panel
    st.subheader("Extras Panel")
    e1, e2 = st.columns(2)
    with e1:
      st.metric("Win Rate", "—")
    with e2:
      st.metric("Sortino Ratio", "—")

    e3, e4 = st.columns(2)
    with e3:
      st.metric("Turnover", "—")
    with e4:
      st.metric("No. of Trades", "—")

 # delta for total returns, cagr, sharpe ratio, volatility