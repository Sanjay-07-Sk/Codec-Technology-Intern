import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.sidebar.title("📈 Stock Dashboard")
ticker = st.sidebar.text_input("Enter Stock Symbol", value='AAPL')
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

try:
    stock_data = load_data(ticker, start_date, end_date)

    st.title(f"📊 Stock Dashboard for {ticker.upper()}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name='Close Price'))
    fig.update_layout(title='Closing Price Over Time', xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig)

    st.subheader("📌 Key Statistics")
    st.metric("Latest Close", f"${stock_data['Close'].iloc[-1]:.2f}")
    st.metric("Open", f"${stock_data['Open'].iloc[-1]:.2f}")
    st.metric("High", f"${stock_data['High'].iloc[-1]:.2f}")
    st.metric("Low", f"${stock_data['Low'].iloc[-1]:.2f}")
    st.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,}")


    with st.expander("🧾 Show Raw Data"):
        st.dataframe(stock_data)

except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")

if stock_data.empty:
    st.warning("No data available for the selected date range.")



