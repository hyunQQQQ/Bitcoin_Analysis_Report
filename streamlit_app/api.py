import requests
from .config import FASTAPI_URL

def get_report():
    """
    FastAPI 서버로부터 투자 보고서 데이터 조회
    """
    return requests.get(f"{FASTAPI_URL}/report").json()

def get_year_range():
    """
    FastAPI 서버로부터 52주 최고가/최저가 조회
    """
    return requests.get(f"{FASTAPI_URL}/year_high_low").json()

def get_ohlcv(days=30):
    """
    업비트 API에서 일봉 기준 OHLCV 데이터 조회
    - days: 조회할 일수 (최대 200일)
    """
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": days}
    return requests.get(url, params=params).json()
