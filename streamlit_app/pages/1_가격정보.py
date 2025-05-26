import sys
import os
# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import websocket
import json
import time
import plotly.graph_objects as go
from streamlit_app.api import get_year_range, get_ohlcv

# 페이지 제목
st.title("실시간 비트코인 가격 정보")

# 1. 52주 고가 / 저가 지표
st.subheader("📅 52주 최고가/최저가")
year_range = get_year_range()
if year_range:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📈 52주 최고가", value=f"{year_range['52week_high']:,} KRW")
    with col2:
        st.metric(label="📉 52주 최저가", value=f"{year_range['52week_low']:,} KRW")
else:
    st.error("📅 52주 고가/저가 데이터를 가져오지 못했습니다.")

st.markdown("---")

# 2. 실시간 비트코인 현재가 (WebSocket 이용)
st.markdown(
    "### 🪙 비트코인 현재 가격 "
    "<span style='font-size: 0.8em;'>- 업비트 기준 실시간 가격 데이터를 2초 간격으로 갱신합니다.</span>",
    unsafe_allow_html=True
)
placeholder = st.empty()

try:
    # WebSocket 연결 및 실시간 가격 수신
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

# 3. 최근 30일 일봉 캔들 차트
st.subheader("📈 최근 30일 BTC Daily Chart")
try:
    ohlcv_data = get_ohlcv(30)
    # 날짜 및 시세 데이터 추출
    dates = [item["candle_date_time_kst"][:10] for item in reversed(ohlcv_data)]
    opens = [item["opening_price"] for item in reversed(ohlcv_data)]
    highs = [item["high_price"] for item in reversed(ohlcv_data)]
    lows = [item["low_price"] for item in reversed(ohlcv_data)]
    closes = [item["trade_price"] for item in reversed(ohlcv_data)]

    # 캔들차트 구성
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
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.error("일봉차트 데이터를 가져오지 못했습니다.")
