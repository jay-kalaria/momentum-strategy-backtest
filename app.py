from core.helper import calc_cagr, calc_sharpe, calc_volatility, calc_sortino
import streamlit as st
import pandas as pd
from core.backtester import walk_forward
import datetime
from stock_ticker_templates import templates
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Momentum Strategy Backtester")
st.write("Configure your parameters in the sidebar and run the strategy.")

names = templates[0].keys()

if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = "AAPL,MSFT,AMZN"
if "selected_benchmark" not in st.session_state:
    st.session_state.selected_benchmark = "SPY"
if "results_show" not in st.session_state:
    st.session_state.results_show = False


if not st.session_state.results_show:
    for i, template in enumerate(templates):
        with st.container(border=True):
            st.subheader("".join(template.keys()))
            cateogry_dict = list(template.values())[0]
            st.write(", ".join(cateogry_dict.keys()))
            if st.button("Select this", key=f"select_template_{i}"):
                selected_tickers = ",".join(cateogry_dict.values())
                st.session_state.selected_tickers = selected_tickers
                st.session_state.results_show = True
                st.rerun()


with st.sidebar.expander("General Parameters", expanded=True):

    # Stock and benchmark selection
    tickers = (
        st.text_input(
            "Ticker (comma separated)",
            value=st.session_state.selected_tickers,
            placeholder="AAPL,MSFT,AMZN",
        )
        .strip()
        .upper()
    )
    benchmark_ticker = (
        st.text_input(
            "Benchmark Ticker",
            value=st.session_state.selected_benchmark,
            placeholder="SPY",
        )
        .strip()
        .upper()
    )

    # Time Period
    start_invest = st.date_input("Starting date", value=pd.to_datetime("2014-01-01"))
    end_invest = st.date_input("Ending date", value=pd.to_datetime("2022-01-01"))

with st.sidebar.expander("General Parameters", expanded=True):
    # Lookback and skip input
    lookback_months = st.number_input(
        "Lookback months",
        min_value=1,
        max_value=24,
        value=6,
        help="Number of months to look back for momentum calculation",
    )
    skip_months = st.number_input(
        "Skip Months",
        min_value=0,
        max_value=6,
        value=1,
        help="Number of months to skip between lookback period and investment",
    )
    start_capital = st.number_input("Start Capital", min_value=100, value=100)

    # Implement
    top_n = st.number_input(
        "Top N Stocks", min_value=1, max_value=len(tickers), value=3
    )
    stop_loss = st.number_input("Stop loss (%) ", min_value=0, value=50)


with st.sidebar:
    run = st.button("Run strategy")
    reset = st.button("Reset")


if reset:
    st.session_state.clear()
    st.rerun()


if run:
    if not tickers or not benchmark_ticker or not start_invest or not end_invest:
        st.error(
            "Please enter valid ticker symbols for both the strategy and benchmark."
        )
        st.stop()

    with st.spinner("Running backtest...This may take a few moments"):
        try:
            (
                trade_records,
                capital,
                ben_capital,
                str_mon_returns,
                ben_mon_returns,
                portfolio_value,
                benchmark_value,
                max_drawdown,
                max_drawdown_ben,
                total_trades,
                wins,
                not_found,
                not_found_ben,
            ) = walk_forward(
                tickers,
                benchmark_ticker,
                start_invest,
                end_invest,
                lookback_months,
                skip_months,
                start_capital,
                stop_loss,
            )

            sharpe = calc_sharpe(str_mon_returns, 0.04)
            cagr = calc_cagr(
                start_capital, capital, str_mon_returns, start_invest, end_invest
            )
        except Exception as e:
            st.error(f"Backtest failed: {e}")
            st.session_state.results_show = False
            st.stop()

    # Set results_show to True after successful backtest
    st.session_state.results_show = True

    total_returns = (((capital - start_capital) / start_capital) * 100).round(2)

    if not_found:
        st.error(
            f"The following tickers could not be found: {not_found}. Please verify the ticker symbols or note that data might be unavailable for the selected period."
        )
    if not_found_ben:
        st.error(
            f"The following benchmark ticker could not be found: {not_found_ben}. Please verify the ticker symbol or note that data might be unavailable for the selected period."
        )
    # st.success("Backtest completed!")

    (tab1,) = st.tabs(["Result and Comparsion"])

    # Generate monthly date range for x-axis based on portfolio values
    # Portfolio values are recorded monthly, so create corresponding dates
    start_date = pd.to_datetime(start_invest)
    dates = pd.date_range(start=start_date, periods=len(portfolio_value), freq="M")

    # Create DataFrame with dates as index for proper x-axis labeling
    graph_data = pd.DataFrame(
        {"Momentum Strategy": portfolio_value, "Benchmark": benchmark_value},
        index=dates,
    )

    # with tab2:
    #     st.subheader("Trade Records")

    #     # Convert to DataFrame and handle any data issues
    #     try:
    #         df_trades = pd.DataFrame(trade_records)

    #         # Separate individual trades from summary rows
    #         individual_trades = df_trades[df_trades["ticker"] != "SUMMARY"].copy()
    #         summary_rows = df_trades[df_trades["ticker"] == "SUMMARY"].copy()

    #         if not individual_trades.empty:
    #             st.write(f"**Individual Trades ({len(individual_trades)} total)**")
    #             st.dataframe(individual_trades, width="stretch")

    #             if not summary_rows.empty:
    #                 st.write("**Summary Rows**")
    #                 st.dataframe(summary_rows, width="stretch")
    #             else:
    #                 st.dataframe(df_trades, width="stretch")

    #     except Exception as e:
    #         st.error(f"Error displaying trade records: {str(e)}")
    #         st.write("Raw trade records:")
    #         st.write(trade_records)

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

        # Create Plotly chart with better axis formatting
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=graph_data.index,
                y=graph_data["Momentum Strategy"],
                mode="lines",
                name="Momentum Strategy",
                line=dict(color="#1f77b4", width=2),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=graph_data.index,
                y=graph_data["Benchmark"],
                mode="lines",
                name="Benchmark",
                line=dict(color="#ff7f0e", width=2),
            )
        )

        # Calculate appropriate tick interval based on data range
        num_months = len(graph_data)
        if num_months <= 12:
            dtick = "M1"
        elif num_months <= 24:
            dtick = "M2"
        else:
            dtick = "M3"
        fig.update_xaxes(
            title_text="Date",
            tickformat="%b %Y",
            tickangle=-45,
            dtick=dtick,
            showgrid=True,
        )

        fig.update_yaxes(
            title_text="Portfolio Value ($)",
            tickformat="$,.0f",
            showgrid=True,
        )

        fig.update_layout(
            title="Portfolio Performance Over Time",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode="x unified",
            height=500,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        st.plotly_chart(fig, use_container_width=True)

        # Performance Panel
        st.subheader("Performance Panel")
        p1, p2 = st.columns(2)
        with p1:
            st.metric("Strategy Total Return", f"{total_returns:.2f}%")
        with p2:
            benchmark_total_return = (
                (ben_capital - start_capital) / start_capital
            ) * 100
            st.metric("Benchmark Total Return", f"{benchmark_total_return:.2f}%")

        p3, p4 = st.columns(2)
        with p3:
            st.metric("Strategy CAGR", f"{cagr:.2%}")
        with p4:
            benchmark_cagr = calc_cagr(
                start_capital, ben_capital, ben_mon_returns, start_invest, end_invest
            )
            st.metric("Benchmark CAGR", f"{benchmark_cagr:.2%}")

        # Risk-Adjusted Panel
        st.subheader("Risk-Adjusted Panel")
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Strategy Sharpe", f"{sharpe:.2f}")
        with r2:
            benchmark_sharpe = calc_sharpe(ben_mon_returns, 0.04)
            st.metric("Benchmark Sharpe", f"{benchmark_sharpe:.2f}")

        r3, r4 = st.columns(2)
        with r3:
            strategy_volatility = calc_volatility(str_mon_returns)
            st.metric("Volatility (Strategy)", f"{strategy_volatility:.2%}")
        with r4:
            benchmark_volatility = calc_volatility(ben_mon_returns)
            st.metric("Volatility (Benchmark)", f"{benchmark_volatility:.2%}")

        r5, r6 = st.columns(2)
        with r5:
            st.metric("Max Drawdown (Strategy)", f"{max_drawdown:.2%}")
        with r6:
            st.metric("Max Drawdown (Benchmark)", f"{max_drawdown_ben:.2%}")

        st.subheader("Extras Panel")
        e1, e2 = st.columns(2)
        with e1:
            strategy_sortino = calc_sortino(str_mon_returns, 0.04)
            st.metric("Sortino Ratio (Strategy)", f"{strategy_sortino:.2f}")
        with e2:
            benchmark_sortino = calc_sortino(ben_mon_returns, 0.04)
            st.metric("Sortino Ratio (Benchmark)", f"{benchmark_sortino:.2f}")

        e3, e4 = st.columns(2)
        with e3:
            win_rate = (wins / total_trades) if total_trades > 0 else 0
            st.metric("Win Rate", f"{win_rate:.2%}")
        with e4:
            st.metric("No. of Trades", f"{total_trades}")

# delta for total returns, cagr, sharpe ratio, volatility
