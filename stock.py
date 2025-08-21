import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")
st.title("🇮🇳 Indian Stock Market: Forecast | History")

# User input for stock ticker
stock = st.text_input(
    "Enter NSE/BSE Ticker (e.g., TCS.NS, RELIANCE.NS):", "RELIANCE.NS"
)

# Historical Data Section
st.header("📈 Historical Data")
period = st.selectbox(
    "Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"], index=3
)
interval = st.selectbox(
    "Interval", ["1d", "1wk", "1mo"], index=0
)

data = pd.DataFrame()

if st.button("Show Data"):
    try:
        data = yf.download(stock, period=period, interval=interval,auto_adjust=False)
        st.write("Data columns:", data.columns)
        st.write(data.tail())
        if 'Close' in data.columns:
            st.line_chart(data['Close'])
            # Calculate SMA here after data is loaded successfully
            window = st.slider("Moving Average Window (days)", 5, 60, 20, key='sma_window')
            data['SMA'] = data['Close'].rolling(window=window).mean()
            st.header("🔮 Simple Forecast (SMA)")
            st.line_chart(data[['Close', 'SMA']])
        else:
            st.error("‘Close’ column not found in data. Please check the ticker symbol.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.info("Enter a ticker symbol and hit 'Show Data' to load historical prices and forecast.")

st.markdown("---")
st.markdown(
    "*This dashboard shows historical stock price data and a simple moving average forecast. "
    "News functionality is omitted to avoid requiring an API key.*"
)
