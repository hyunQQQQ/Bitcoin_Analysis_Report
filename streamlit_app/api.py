import requests
from .config import FASTAPI_URL

def safe_get_json(url, params=None, headers=None, timeout=60):
    """
    안정적인 외부 API 호출 유틸 함수
    - 실패 시 dict 또는 list 반환
    """
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except:
        # 업비트처럼 list 응답이 기본인 경우에는 [] 반환
        return [] if "upbit" in url or "/candles" in url else {}

def get_report():
    """
    FastAPI 서버로부터 투자 보고서 데이터 조회
    """
    return safe_get_json(f"{FASTAPI_URL}/report")

def get_year_range():
    """
    FastAPI 서버로부터 52주 최고가/최저가 조회
    """
    return safe_get_json(f"{FASTAPI_URL}/year_high_low")

def get_ohlcv(days=30):
    """
    업비트 API에서 일봉 기준 OHLCV 데이터 조회
    - days: 조회할 일수 (최대 200일)
    """
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": days}
    return safe_get_json(url, params=params)
