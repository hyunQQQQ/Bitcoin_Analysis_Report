#투자의견견
import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.title("종합 분석 / 투자 의견")

report_response = requests.get(f"{FASTAPI_URL}/report")
if report_response.status_code == 200:
    report_data = report_response.json()
    st.markdown(report_data["investment_report"])
else:
    st.error("투자 의견 데이터를 가져오지 못했습니다.")
