import streamlit as st
from streamlit_app.api import get_report

# 페이지 제목
st.title("최신 뉴스 및 요약")

# FastAPI로부터 뉴스 요약 데이터 수신
report_data = get_report()

if report_data:
    # 요약된 뉴스 리스트 출력
    for idx, news in enumerate(report_data['news']):
        st.markdown(f"### {idx+1}. {news['title']}")
        st.markdown(f"[기사 링크]({news['url']})")
        st.write(f"요약: {news['summary']}")
        st.markdown("---")
else:
    st.error("뉴스 데이터를 가져오지 못했습니다.")
