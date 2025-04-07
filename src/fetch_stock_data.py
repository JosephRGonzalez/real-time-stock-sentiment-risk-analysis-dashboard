import yfinance as yf
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(symbol, period='30d', interval='1h'):
    return yf.download(symbol, period=period, interval=interval)

