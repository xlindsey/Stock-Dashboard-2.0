import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

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

# --- Show Last Updated Time ---
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Fetch Data ---
def get_data(tickers):
    data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker', threads=True)
    summary = []
    for ticker in tickers:
        try:
            last_price = data[ticker]['Close'][-1]
            prev_close = yf.Ticker(ticker).info.get("previousClose", 0)
            pct_change = ((last_price - prev_close) / prev_close) * 100 if prev_close else 0
            intraday = data[ticker]['Close'][-10:].tolist() if len(data[ticker]['Close']) >= 10 else data[ticker]['Close'].tolist()

            summary.append({
                "Ticker": ticker,
                "Price": round(last_price, 2),
                "Change (%)": round(pct_change, 2),
                "Chart": intraday
            })
        except Exception as e:
            summary.append({
                "Ticker": ticker,
                "Price": "Error",
                "Change (%)": "Error",
                "Chart": []
            })
    return pd.DataFrame(summary)

df = get_data(tickers)

# --- Color % Change and Add Sparklines ---
def format_row(row):
    color = "green" if isinstance(row["Change (%)"], (int, float)) and row["Change (%)"] > 0 else "red"
    return f'<span style="color:{color}">{row["Change (%)"]}%</span>'

df["Change (%)"] = df.apply(format_row, axis=1)
df["Chart"] = df["Chart"].apply(lambda x: st._legacy_sparklines.sparkline(x) if x else "-")

# --- Show Table ---
st.write("### 📊 Stock Summary")
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
