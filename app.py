import streamlit as st
import pandas as pd
from core.backtester import walk_forward

st.title("Momentum Strategy Dashboard")
st.write("Select parameters and see portfolio returns")

with st.sidebar:
  st.header("Parameters")

  #Period
  start_invest = st.date_input("Starting date")
  end_invest = st.date_input("Ending date")

  # Lookback and skip input
  lookback_months= st.number_input("Lookback months", min_value=1 , max_value=24, value=6)
  skip_months = st.number_input("Skip Months", min_value=0 , max_value=6, value=1)
  start_capital = st.number_input("Start Capital", min_value=100 , value=100 )
  run = st.button("Run strategy")
  reset = st.button("Reset")

# Run strategy
if run:
  trade_records = walk_forward(start_invest, end_invest, lookback_months, skip_months, start_capital)
  st.subheader("Results")
  st.dataframe(trade_records)

# Reset button
if reset:
  st.session_state.clear()