import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Stock Dashboard", layout="wide")

# --- Load tickers from Google Sheets ---
sheet_url = "https://docs.google.com/spreadsheets/d/1vB3Ttv3Rqlo3yUFU2iESWFNAtqK9SCB7VerQWqB9spM/export?format=csv"

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

st.title("📈 My Stock Dashboard")

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
        except Exception:
            summary.append({
                "Ticker": ticker,
                "Price": "Error",
                "Change (%)": "Error"
            })
    return pd.DataFrame(summary)

df = get_data(tickers)
st.dataframe(df, use_container_width=True)
