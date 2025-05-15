#  Bitcoin_Analysis_Report

업비트 API, 네이버 뉴스 API, OpenAI GPT를 활용한 **비트코인 투자 분석 보고서 자동 생성 및 시각화 프로젝트**입니다.  
FastAPI 백엔드 + Streamlit 프론트엔드 기반으로 구성되며, 실시간 가격 확인과 최신 뉴스 요약, 투자 의견 작성까지 지원합니다.

---

##  기술 스택

- **Backend**: FastAPI, OpenAI API, Naver API
- **Frontend**: Streamlit, Plotly
- **데이터 출처**:
  - 업비트 API (실시간 가격, 일봉/주봉/월봉 차트)
  - 네이버 뉴스 API (최신 비트코인 관련 기사)
  - OpenAI GPT (뉴스 요약, 투자 의견 생성)

---

##  프로젝트 구조

```
Bitcoin_Analysis_Report/
├── app/                    # FastAPI 백엔드
│   ├── main.py
│   └── __init__.py
├── streamlit_app/          # Streamlit 프론트엔드
│   ├── app.py
│   └── pages/
│       ├── 1_가격정보.py
│       ├── 2_뉴스요약.py
│       └── 3_투자의견.py
├── .env                    # API 키 저장
├── requirements.txt        # 패키지 목록
└── README.md               # 설명 문서
```

---

##  실행 방법

### 1. 가상환경 생성 및 실행
```bash
python -m venv venv
source venv/bin/activate    # (Windows: venv\Scripts\activate)
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (.env 파일)
```
OPENAI_API_KEY=your_openai_key
NAVER_CLIENT_ID=your_naver_id
NAVER_CLIENT_SECRET=your_naver_secret
```

### 4. FastAPI 서버 실행
```bash
uvicorn app.main:app --reload
```

### 5. Streamlit 앱 실행
```bash
streamlit run streamlit_app/app.py
```

---

##  주요 기능
| 기능                 | 설명 |
|----------------------|------|
| 실시간 가격 조회   | WebSocket을 통한 실시간 시세 표시 |
| 비트코인 뉴스 요약 | 네이버 뉴스 + GPT 요약 |
| 투자 보고서 생성   | GPT 기반 종합 분석 및 의견 자동 생성 |
| 캔들 차트 시각화   | Plotly로 최근 1개월 월봉 차트 표시 |

---

## 주의사항

- `.env` 파일은 `.gitignore`에 포함되어 있어야 합니다.

---
