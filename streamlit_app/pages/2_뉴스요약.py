#뉴스요약약
import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.title("최신 뉴스 및 요약")

report_response = requests.get(f"{FASTAPI_URL}/report")
if report_response.status_code == 200:
    report_data = report_response.json()

    for idx, news in enumerate(report_data['news']):
        st.markdown(f"### {idx+1}. {news['title']}")
        st.markdown(f"[기사 링크]({news['url']})")
        st.write(f"요약: {news['summary']}")
        st.markdown("---")
else:
    st.error("뉴스 데이터를 가져오지 못했습니다.")
