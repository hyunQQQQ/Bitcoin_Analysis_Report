# 투자의견
import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.title("종합 분석 / 투자 의견")

report_response = requests.get(f"{FASTAPI_URL}/report")
if report_response.status_code == 200:
    report_data = report_response.json()
    investment_report = report_data.get("investment_report")

    if isinstance(investment_report, dict) and "price_trend" in investment_report:
        st.markdown("### 가격 동향")
        st.write(investment_report["price_trend"])

        st.markdown("### 주요 이슈")
        st.write(investment_report["key_issues"])

        st.markdown("### 시장 분석")
        st.write(investment_report["market_analysis"])

        st.markdown("### 리스크 요인")
        for risk in investment_report.get("risk_factors", []):
            st.write(f"- {risk}")

        st.markdown("### 종합 의견")
        st.write(investment_report["final_opinion"])
    else:
        # 기존 마크다운 형식 출력 (백업 대응)
        st.markdown(investment_report)
else:
    st.error("투자 의견 데이터를 가져오지 못했습니다.")
