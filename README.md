# Bitcoin Analysis Report

FastAPI + Streamlit 기반의 비트코인 실시간 분석 및 투자 보고서 생성 프로젝트입니다.
업비트 시세, 네이버 뉴스, OpenAI를 기반으로 실시간 정보 제공과 GPT 기반 투자 의견서를 생성합니다.

---

## 프로젝트 구조

```
Bitcoin_Analysis_Report/
├── app/
│   ├── main.py                  # FastAPI Main
│   └── services/                # 비즈니스 로직 분리
│       ├── gpt.py
│       ├── news.py
│       ├── market.py
│       └── websocket.py
├── streamlit_app/
│   ├── app.py                   # Streamlit Main
│   ├── api.py                   # FastAPI API 호출 함수들
│   ├── config.py                # 공통 설정값
│   └── pages/
│       ├── 1_가격정보.py
│       ├── 2_뉴스요약.py
│       └── 3_투자의견.py
├── .env                         # 환경변수 설정
├── requirements.txt
└── README.md
```

---

## 설치 및 실행

### 가상환경 설정 및 패키지 설치

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### .env 설정 예시

```
NAVER_CLIENT_ID=YOUR_NAVER_CLIENT_ID
NAVER_CLIENT_SECRET=YOUR_NAVER_CLIENT_SECRET
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

### FastAPI 실행 (포트 8000)

```bash
uvicorn app.main:app --reload
```

### Streamlit 실행 (포트 8501)

> 반드시 PYTHONPATH를 지정해야 함 (PowerShell 기준)

```powershell
cd C:\Bitcoin_Analysis_Report
$env:PYTHONPATH = $PWD
streamlit run streamlit_app/app.py
```

---

## 주요 기능

* **실시간 가격**: 업비트 WebSocket API를 이용한 실시간 가격 수신
* **가격 차트**: 30일 일봉 기반 캔들 차트 시각화 (Plotly)
* **뉴스 요약**: 네이버 뉴스 + 본문 크롤링 + GPT 요약 처리
* **투자 보고서**: Structured JSON 형식으로 GPT 기반 종합 분석 생성

---

## 사용 기술

* `FastAPI`, `Streamlit`, `OpenAI GPT API`
* `Upbit API`, `Naver OpenAPI`
* `Plotly`, `websocket-client`, `requests`

---

## 주의사항

* 반드시 FastAPI 서버를 먼저 실행해야 Streamlit이 연결할 수 있습니다.
* `.env` 파일 누락 시 GPT 및 뉴스 요약 기능이 정상 동작하지 않습니다.

---


## 기술 문제 해결

- **1. GPT 모델로부터 Structured JSON 응답을 안정적으로 파싱하는 방식 설계**  
  OpenAI GPT-3.5-turbo를 활용해 투자 보고서를 자동 생성할 때,  
  "가격 동향, 이슈, 시장 분석, 리스크, 종합 의견" 구조의 JSON을 명세하여 프롬프트에 반영.  
  응답 파싱 실패 시 대비해 `json.loads()` 예외 처리를 추가하고,  
  실패한 경우 raw 응답도 함께 반환해 디버깅 및 유저 피드백이 가능하도록 설계.

- **2. 네이버 뉴스 본문 크롤링 안정성 강화**  
  네이버 뉴스 API에서 제공하는 링크 중 본문 크롤링이 가능한 경우(`n.news.naver.com`)만 필터링.  
  `div#newsct_article`, `#articleBodyContents` 등 다양한 구조에 대응하며,  
  본문이 너무 짧거나 없을 경우 GPT 요약을 생략하거나 경고 처리하도록 설계.

- **3. Plotly를 활용한 최근 30일 비트코인 캔들 차트 시각화 구현**  
  업비트 OHLCV API 데이터를 기반으로 Plotly의 `go.Candlestick()`을 활용해  
  실제 금융 리포트 스타일의 차트를 구현.  
  날짜 축 정렬, 상승/하락 색상 지정, margin 최적화 등 사용자 시각 편의를 고려하여 구성.

- **4. WebSocket 기반 실시간 비트코인 시세 반영 구현 (업비트 + Plotly)**  
  업비트의 WebSocket API를 통해 실시간 가격 데이터를 받아  
  Streamlit 상단에 현재가를 즉시 반영.  
  연결 오류나 수신 지연 발생 시 자동 복구 처리를 위해 예외 처리와 스레드 기반 실행을 적용.

- **5. 투자 보고서 구조화(JSON)와 마크다운 대응 전략 이중화**  
  LLM 응답 형식을 Structured JSON으로 유도하되,  
  예외 상황에서는 기존 마크다운 기반 응답도 허용하여 UI 중단 없이 대응할 수 있도록 백업 출력 방식을 설계.
