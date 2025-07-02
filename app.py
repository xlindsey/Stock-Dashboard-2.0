import streamlit as st
import yfinance as yf
import pandas as pd

# Favorite stock tickers
TICKERS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

st.title("📈 My Stock Dashboard")

# Fetch and display stock data
def get_data(tickers):
    data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker', threads=True)
    summary = []

    for ticker in tickers:
        last_price = data[ticker]['Close'][-1]
        prev_close = yf.Ticker(ticker).info.get("previousClose", 0)
        pct_change = ((last_price - prev_close) / prev_close) * 100 if prev_close else 0

        summary.append({
            "Ticker": ticker,
            "Price": round(last_price, 2),
            "Change (%)": round(pct_change, 2)
        })

    return pd.DataFrame(summary)

df = get_data(TICKERS)
st.dataframe(df, use_container_width=True)
