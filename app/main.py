import requests
from fastapi import FastAPI, WebSocket
from bs4 import BeautifulSoup
import html
from dotenv import load_dotenv
import os
import openai
import asyncio
from fastapi import WebSocket
import time
import json
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

# .env 환경변수 로드
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

#뉴스요약 토글 
ENABLE_NEWS_SUMMARY = True

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.get("/price")
def get_price():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data[0]["trade_price"],
        "high": data[0]["high_price"],
        "low": data[0]["low_price"],
        "change_rate": data[0]["signed_change_rate"]
    }

@app.get("/news")
def get_news():
    return get_naver_news_api()

@app.get("/report")
def get_report():
    news_data = get_naver_news_api()
    summarized_news = []
    all_summaries = []

    for item in news_data:
        content = get_article_content(item['url'])

        if ENABLE_NEWS_SUMMARY:
            if not content or len(content) < 100:
                summary = "기사 본문 크롤링 실패: 내용 부족"
            else:
                summary = summarize_text(content)
        else:
            summary = "요약 기능 비활성화됨"

        all_summaries.append(summary)
        summarized_news.append({
            "title": item['title'],
            "url": item['url'],
            "summary": summary
        })

    combined_summary = "\n".join(all_summaries)

    investment_comment = summarize_text(
        f"""
        당신은 비트코인 전문 리서치센터 소속 애널리스트입니다.
        다음은 최근 비트코인 관련 뉴스 요약입니다:

        {combined_summary}

        이 요약을 기반으로, 다음 조건을 모두 만족하는 투자 의견서를 작성해 주세요:
        - 실제 증권사, 리서치 기관에서 발행하는 투자 보고서 형식        
        - 3문단 정도        
        - 문체: 전문적이고 객관적, 분석적인 문체
        - 내용: 현재 가격 동향, 주요 이슈, 시장 분석, 리스크 요인, 종합 의견
        - 마크다운 형식으로
        """
    )

    price_data = get_price()

    return {
        "price": price_data,
        "news": summarized_news,
        "investment_report": investment_comment
    }

@app.get("/ohlcv")
def get_ohlcv_endpoint():
    return get_bitcoin_ohlcv()

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = get_price()
            await websocket.send_json(data)
            await asyncio.sleep(1)
        except Exception as e:
            await websocket.close()
            break

def get_bitcoin_ohlcv():
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": 7}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_naver_news_api():
    query = "비트코인"
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=100"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        news_list = []
        for item in data['items']:
            if "n.news.naver.com" in item['link']:
                title_unescaped = html.unescape(item['title'])
                title_clean = BeautifulSoup(title_unescaped, "html.parser").get_text()
                news_list.append({
                    "title": title_clean,
                    "url": item['link']
                })
                if len(news_list) == 10:
                    break
        return news_list
    else:
        return []

def get_article_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body = (
        soup.select_one('div#newsct_article') or
        soup.select_one('div#articeBody') or
        soup.select_one('div#articleBodyContents')
    )
    if article_body:
        return article_body.get_text(strip=True)
    else:
        return ""

def summarize_text(text):
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


@app.websocket("/ws/price")
async def websocket_price_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
            response = requests.get(url)
            data = response.json()[0]
            await websocket.send_json({
                "price": data["trade_price"],
                "timestamp": data["timestamp"]
            })
            await asyncio.sleep(2)  # 2초마다 업데이트
    except WebSocketDisconnect:
        print("WebSocket 연결 종료됨")

@app.get("/year_high_low")
def get_year_high_low():
    url = "https://api.upbit.com/v1/candles/days"
    params = {"market": "KRW-BTC", "count": 365}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        highs = [day['high_price'] for day in data]
        lows = [day['low_price'] for day in data]
        return {
            "52week_high": max(highs),
            "52week_low": min(lows)
        }
    else:
        return {"error": "데이터 조회 실패"}
