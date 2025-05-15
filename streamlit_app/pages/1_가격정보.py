#가격정보
import streamlit as st
import websocket
import json
import time
import requests
import plotly.graph_objects as go

FASTAPI_URL = "http://localhost:8000"

st.title("실시간 비트코인 가격 정보")

# 1. 52주 고가/저가
st.subheader("📅 52주 최고가/최저가")
year_range_response = requests.get(f"{FASTAPI_URL}/year_high_low")
if year_range_response.status_code == 200:
    year_range = year_range_response.json()
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📈 52주 최고가", value=f"{year_range['52week_high']:,} KRW")
    with col2:
        st.metric(label="📉 52주 최저가", value=f"{year_range['52week_low']:,} KRW")
else:
    st.error("📅 52주 고가/저가 데이터를 가져오지 못했습니다.")
st.markdown("---")

# 2. 실시간 현재가
st.markdown("""### 🪙 비트코인 현재 가격 <span style='font-size: 0.8em;'>- 업비트 기준 실시간 가격 데이터를 2초 간격으로 갱신합니다.</span>""", unsafe_allow_html=True)
placeholder = st.empty()

try:
    ws = websocket.create_connection("wss://api.upbit.com/websocket/v1")
    ws.send(json.dumps([
        {"ticket": "test"},
        {"type": "ticker", "codes": ["KRW-BTC"]}
    ]))
    result = ws.recv()
    data = json.loads(result)
    price = data.get('trade_price', None)
    if price:
        placeholder.metric(label="", value=f"{price:,.0f} KRW")
    ws.close()
except Exception as e:
    st.error(f"WebSocket 연결 오류: {e}")

st.markdown("---")
# 3. 최근 30일 일봉 기반 캔들차트
st.subheader("📈 최근 30일 BTC Daily Chart")
ohlcv_url = "https://api.upbit.com/v1/candles/days"
params = {"market": "KRW-BTC", "count": 30}
ohlcv_response = requests.get(ohlcv_url, params=params)
if ohlcv_response.status_code == 200:
    ohlcv_data = ohlcv_response.json()

    dates = [item["candle_date_time_kst"][:10] for item in reversed(ohlcv_data)]
    opens = [item["opening_price"] for item in reversed(ohlcv_data)]
    highs = [item["high_price"] for item in reversed(ohlcv_data)]
    lows = [item["low_price"] for item in reversed(ohlcv_data)]
    closes = [item["trade_price"] for item in reversed(ohlcv_data)]

    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=opens,
        high=highs,
        low=lows,
        close=closes,
        increasing_line_color='red',
        decreasing_line_color='blue'
    )])

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="가격 (KRW)",
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)  # 좌우 여백 줄이기
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("일봉차트트 데이터를 가져오지 못했습니다.")
