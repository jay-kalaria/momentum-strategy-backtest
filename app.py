import streamlit as st
import pandas as pd

st.title("Momentum Strategy Dashboard")
st.write("Select parameters and see portfolio returns")


# Period

start_date = st.sidebar.date_input("Starting date")
end_date = st.sidebar.date_input("Ending date")



# Lookback and skip input
lookback= st.sidebar.number_input("Lookback months", min_value=1 , max_value=24, value=6)
skip_months = st.sidebar.number_input("Skip Months", min_value=0 , max_value=6, value=1)


def run_strategy():
  data ={
    "Ticker":  ["GOOG","MSFT","AAPL"],
    "return": [5.6, 1.4,5.7]         
  }
  return data

# Button to run strategy
if st.sidebar.button("Run Strategy"):
  st.success("Running")
  results = run_strategy()
  st.subheader("Results")
  st.dataframe(results)

# Reset button
if st.sidebar.button("Reset"):
  st.session_state.clear()