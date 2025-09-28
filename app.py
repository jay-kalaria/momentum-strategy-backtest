import streamlit as st
import pandas as pd
from core.backtester import walk_forward
import datetime

st.title("Momentum Strategy Backtester with")
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
    trade_records, capital, ben_capital = walk_forward(start_invest, end_invest, lookback_months, skip_months, start_capital)
  
  st.success("Backtest completed!"
  )
  tab1,tab2,tab3 = st.tabs(["Result and Comparsion","Monthly Performace","Detailed Analysis"])


  with tab1:
    st.header("Results")
    st.subheader("Results")
    st.metric(label="Strategy Capital", value=capital)
    st.metric(label="Benchmark Capital", value=ben_capital)
    st.dataframe(trade_records)

