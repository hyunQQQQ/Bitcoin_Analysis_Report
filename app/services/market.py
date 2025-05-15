import requests

def get_price():
    """
    현재 비트코인 시세 정보 조회 (Upbit API)
    """
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data[0]["trade_price"],         # 현재가
        "high": data[0]["high_price"],           # 당일 고가
        "low": data[0]["low_price"],             # 당일 저가
        "change_rate": data[0]["signed_change_rate"]  # 전일 대비 등락률
    }

def get_ohlcv(days=7):
    """
    일봉 기준 OHLCV 데이터 조회 (최근 N일)
    """
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": days}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def get_52week_range():
    """
    최근 1년간 최고가 / 최저가 계산
    """
    data = get_ohlcv(365)
    if not data:
        return {"error": "데이터 조회 실패"}

    highs = [day['high_price'] for day in data]
    lows = [day['low_price'] for day in data]
    return {
        "52week_high": max(highs),
        "52week_low": min(lows)
    }
