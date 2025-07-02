import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Stock Dashboard", layout="wide")

# Default watchlist (you can replace this later)
default_tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

st.title("📈 My Stock Dashboard")

# --- Load tickers from Google Sheets ---
sheet_url = "https://docs.google.com/spreadsheets/d/1v83Ttv3Rqlo3YUfU2iESWFWAtqK95CB7V0rQWqB9spM/export?format=csv"

@st.cache_data(ttl=300)
def load_tickers_from_gsheet(url):
    try:
        df = pd.read_csv(url)
        tickers = df.iloc[:, 0].dropna().astype(str).str.upper().tolist()
        return tickers
    except Exception as e:
        st.error(f"Failed to load tickers from Google Sheets: {e}")
        return []

tickers = load_tickers_from_gsheet(sheet_url)


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
def style_change_column(change):
    try:
        change = float(change)
        color = "green" if change > 0 else "red"
        return f'<span style="color:{color}">{change:.2f}%</span>'
    except:
        return f'<span>{change}</span>'

