import streamlit as st
import requests

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
else:
    st.error("가격 데이터를 가져오지 못했습니다.")

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