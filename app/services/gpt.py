import openai
import os
import json
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 설정
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    """
    입력 텍스트를 한 문단으로 요약
    """
    if not text:
        return "본문 없음"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "다음 뉴스 기사를 한 문단으로 요약해줘."},
            {"role": "user", "content": text}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def generate_structured_report(summary: str) -> dict:
    """
    뉴스 요약을 기반으로 투자 보고서 JSON 생성
    """
    prompt = f"""
너는 비트코인 전문 리서치센터의 시니어 애널리스트야.

다음은 최근 비트코인 관련 뉴스 요약이야:

{summary}

아래 JSON 구조에 맞춰 투자 의견서를 작성해 줘. 
각 항목은 간결하면서도 분석적으로 작성되야 하고, 반드시 올바른 JSON 형식으로만 응답해.
final_opinion은 500자 정도로 심층적으로 작성해줘.

{{
  "price_trend": "비트코인 가격의 최근 흐름 요약",
  "key_issues": "최근 주요 이슈와 뉴스 요약",
  "market_analysis": "기술적 분석과 투자심리에 대한 평가",
  "risk_factors": ["리스크 요인1", "리스크 요인2"],
  "final_opinion": "최종 종합 의견 및 투자 전략"
}}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 투자 리서치 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1600
    ).choices[0].message.content.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": "JSON 파싱 실패", "raw_response": response}
