import os
from dotenv import load_dotenv

# ✅ 반드시 가장 먼저 환경변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
print("✅ STREAMLIT LOAD TEST - NAVER_CLIENT_ID:", os.getenv("NAVER_CLIENT_ID"))

# ✅ 그 다음에야 streamlit import
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="비트코인 투자 보고서", layout="wide")

# 페이지 제목
st.title("비트코인 투자 보고서 작성기")

# 설명 섹션
st.markdown("""
이 애플리케이션은 FastAPI + Streamlit 기반의 투자 보고서 생성 도구입니다.  
왼쪽 사이드바에서 각 기능별 페이지로 이동할 수 있습니다.

- **가격 정보**: 실시간 비트코인 시세 및 차트  
- **뉴스 요약**: 최신 비트코인 관련 뉴스 및 요약  
- **투자의견**: 뉴스 기반 LLM 요약 및 전문가형 의견서
""")
