import streamlit as st
from streamlit_app.api import get_report

# 페이지 제목
st.title("종합 분석 / 투자 의견")

# FastAPI로부터 분석 리포트 데이터 수신
report_data = get_report()

if report_data:
    investment_report = report_data.get("investment_report")

    # 투자 의견 데이터가 JSON 구조일 경우
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
    
    # JSON 구조가 아닌 경우 (에러 응답 또는 단순 문자열)
    else:
        st.markdown(investment_report)
else:
    st.error("투자 의견 데이터를 가져오지 못했습니다.")
