import sys
import os
# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from streamlit_app.api import get_report

st.title("종합 분석 / 투자 의견")

with st.spinner("투자 리포트를 생성하는 중입니다..."):
    report_data = get_report()

if report_data:
    investment_report = report_data.get("investment_report")

    if isinstance(investment_report, dict) and "price_trend" in investment_report:
        st.markdown("### 가격 동향")
        st.write(investment_report.get("price_trend", "데이터 없음"))
        st.markdown("### 주요 이슈")
        st.write(investment_report.get("key_issues", "데이터 없음"))
        st.markdown("### 시장 분석")
        st.write(investment_report.get("market_analysis", "데이터 없음"))
        st.markdown("### 리스크 요인")
        for risk in investment_report.get("risk_factors", []):
            st.write(f"- {risk}")
        st.markdown("### 종합 의견")
        st.write(investment_report.get("final_opinion", "데이터 없음"))
    else:
        st.markdown(str(investment_report))
else:
    st.error("투자 의견 데이터를 가져오지 못했습니다.")
