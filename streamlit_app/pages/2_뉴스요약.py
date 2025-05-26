import sys
import os
# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from streamlit_app.api import get_report

st.title("최신 뉴스 및 요약")

with st.spinner("뉴스 요약 및 분석 데이터를 생성하는는 중입니다..."):
    report_data = get_report()

if report_data and "news" in report_data:
    for idx, news in enumerate(report_data["news"]):
        st.markdown(f"### {idx+1}. {news.get('title', '제목 없음')}")
        st.markdown(f"[기사 링크]({news.get('url', '#')})")
        st.write(f"요약: {news.get('summary', '요약 없음')}")
        st.markdown("---")
else:
    st.error("뉴스 데이터를 가져오지 못했습니다.")
