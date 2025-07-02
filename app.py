import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Stock Dashboard", layout="wide")

# Default watchlist (you can replace this later)
default_tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

st.title("📈 My Stock Dashboard")

# --- Sidebar Form to Edit Tickers ---
with st.sidebar.form("tickers_form"):
    st.subheader("Edit Your Watchlist")
    tickers_input = st.text_area("Enter tickers (comma-separated):", ",".join(default_tickers))
    submitted = st.form_submit_button("Update")

if submitted:
    tickers = [x.strip().upper() for x in tickers_input.split(",") if x.strip()]
else:
    tickers = default_tickers

# --- Fetch Data ---
def get_data(tickers):
    data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker', threads=True)
    summary = []
    for ticker in tickers:
        try:
            last_price = data[ticker]['Close'][-1]
            prev_close = yf.Ticker(ticker).info.get("previousClose", 0)
            pct_change = ((last_price - prev_close) / prev_close) * 100 if prev_close else 0
            summary.append({
                "Ticker": ticker,
                "Price": round(last_price, 2),
                "Change (%)": round(pct_change, 2)
            })
        except Exception as e:
            summary.append({
                "Ticker": ticker,
                "Price": "Error",
                "Change (%)": "Error"
            })
    return pd.DataFrame(summary)

df = get_data(tickers)
st.dataframe(df, use_container_width=True)
