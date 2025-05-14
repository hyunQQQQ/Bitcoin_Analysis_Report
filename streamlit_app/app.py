import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


FASTAPI_URL = "http://localhost:8000"

st.title("비트코인 투자 보고서(업비트 기준)")

# 가격 정보
st.header("현재 비트코인 가격")
price_response = requests.get(f"{FASTAPI_URL}/price")
if price_response.status_code == 200:
    price_data = price_response.json()
    st.metric(label="현재가", value=f"{price_data['price']:,} KRW")
    st.metric(label="고가", value=f"{price_data['high']:,} KRW")
    st.metric(label="저가", value=f"{price_data['low']:,} KRW")
    st.metric(label="변동률", value=f"{price_data['change_rate'] * 100:.2f}%")

    # ✅ 2. 차트 데이터도 함께 가져오기
    ohlcv_response = requests.get(f"{FASTAPI_URL}/ohlcv")
    if ohlcv_response.status_code == 200:
        ohlcv_data = ohlcv_response.json()
        dates = [item['candle_date_time_kst'][:10] for item in reversed(ohlcv_data)]
        prices = [item['trade_price'] for item in reversed(ohlcv_data)]
        df = pd.DataFrame({'날짜': dates, '종가': prices})

        st.subheader("📊 최근 7일간 비트코인 종가 차트")
        fig, ax = plt.subplots()
        ax.plot(df['날짜'], df['종가'], marker='o', linestyle='-', color='orange')
        ax.set_xlabel("날짜")
        ax.set_ylabel("가격 (KRW)")
        ax.set_title("비트코인 일간 종가 추이")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.error("📉 차트 데이터를 가져오지 못했습니다.")
else:
    st.error("❌ 가격 데이터를 가져오지 못했습니다.")

# 투자 보고서
st.header("📄 최신 뉴스 및 요약")
report_response = requests.get(f"{FASTAPI_URL}/report")
if report_response.status_code == 200:
    report_data = report_response.json()

    for idx, news in enumerate(report_data['news']):
        st.markdown(f"### {idx+1}. {news['title']}")
        st.markdown(f"[기사 링크]({news['url']})")
        st.write(f"요약: {news['summary']}")
        st.write("---")
else:
    st.error("투자 보고서를 가져오지 못했습니다.")

st.header("종합 분석 / 투자 의견")
st.markdown(report_data['investment_report'])