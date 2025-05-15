import requests
from bs4 import BeautifulSoup
import html
import os

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_naver_news_api(query="비트코인", limit=10):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=100"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    news_list = []
    for item in response.json().get('items', []):
        if "n.news.naver.com" in item['link']:
            title_unescaped = html.unescape(item['title'])
            title_clean = BeautifulSoup(title_unescaped, "html.parser").get_text()
            news_list.append({
                "title": title_clean,
                "url": item['link']
            })
            if len(news_list) >= limit:
                break
    return news_list

def get_article_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body = (
        soup.select_one('div#newsct_article') or
        soup.select_one('div#articeBody') or
        soup.select_one('div#articleBodyContents')
    )
    return article_body.get_text(strip=True) if article_body else ""
