# streamlit_app/api.py

import requests
from .config import FASTAPI_URL

def get_report():
    return requests.get(f"{FASTAPI_URL}/report").json()

def get_year_range():
    return requests.get(f"{FASTAPI_URL}/year_high_low").json()

def get_ohlcv(days=30):
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": days}
    return requests.get(url, params=params).json()
