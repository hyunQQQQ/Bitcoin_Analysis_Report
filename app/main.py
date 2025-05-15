import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, WebSocket
from services.news import get_naver_news_api, get_article_content
from services.market import get_price, get_ohlcv, get_52week_range
from services.gpt import summarize_text, generate_structured_report
from services.websocket import send_realtime_price
import asyncio

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.get("/price")
def price():
    return get_price()

@app.get("/ohlcv")
def ohlcv():
    return get_ohlcv()

@app.get("/year_high_low")
def year_high_low():
    return get_52week_range()

@app.get("/news")
def news():
    return get_naver_news_api()

@app.get("/report")
def get_report():
    news_data = get_naver_news_api()
    summarized_news = []
    all_summaries = []

    for item in news_data:
        content = get_article_content(item['url'])
        if not content or len(content) < 100:
            summary = "기사 본문 크롤링 실패: 내용 부족"
        else:
            summary = summarize_text(content)
        all_summaries.append(summary)
        summarized_news.append({
            "title": item['title'],
            "url": item['url'],
            "summary": summary
        })

    combined_summary = "\n".join(all_summaries)
    investment_json = generate_structured_report(combined_summary)

    return {
        "price": get_price(),
        "news": summarized_news,
        "investment_report": investment_json
    }

@app.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    await send_realtime_price(websocket, interval_sec=2)
