import requests

def get_price():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data[0]["trade_price"],
        "high": data[0]["high_price"],
        "low": data[0]["low_price"],
        "change_rate": data[0]["signed_change_rate"]
    }

def get_ohlcv(days=7):
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_52week_range():
    data = get_ohlcv(365)
    if not data:
        return {"error": "데이터 조회 실패"}

    highs = [day['high_price'] for day in data]
    lows = [day['low_price'] for day in data]
    return {
        "52week_high": max(highs),
        "52week_low": min(lows)
    }
