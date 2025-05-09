import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup
import html
from dotenv import load_dotenv
import os
import openai

# .env 환경변수 로드
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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

    for item in news_data:
        content = get_article_content(item['url'])

        if not content or len(content) < 100:
            summary = "기사 본문 크롤링 실패: 내용 부족"
        else:
            summary = summarize_text(content)

        summarized_news.append({
            "title": item['title'],
            "url": item['url'],
            "summary": summary
        })

    price_data = get_price()

    return {
        "price": price_data,
        "news": summarized_news
    }

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
        print(f"API 요청 실패: {response.status_code}")
        return []

def get_article_content(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
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

"""
def summarize_text(text):
    if not text:
        return "본문 없음"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "다음 뉴스 기사를 한 문단으로 요약해줘."},
            {"role": "user", "content": text}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
"""