import requests
from bs4 import BeautifulSoup
import html
import os

# 네이버 API 인증 정보
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_naver_news_api(query="비트코인", limit=10):
    """
    네이버 뉴스 검색 API로 비트코인 관련 뉴스 기사 목록 반환
    - query: 검색 키워드
    - limit: 최대 기사 수 (네이버 기사만 필터링)
    """
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=100"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        items = response.json().get('items', [])
    except:
        return []

    news_list = []
    for item in items:
        if "n.news.naver.com" in item.get('link', ''):
            title_unescaped = html.unescape(item.get('title', ''))
            title_clean = BeautifulSoup(title_unescaped, "html.parser").get_text()
            news_list.append({
                "title": title_clean,
                "url": item['link']
            })
            if len(news_list) >= limit:
                break
    return news_list

def get_article_content(url):
    """
    네이버 뉴스 기사 본문 크롤링
    - 여러 버전의 기사 구조를 대응
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_body = (
            soup.select_one('div#newsct_article') or
            soup.select_one('div#articeBody') or
            soup.select_one('div#articleBodyContents')
        )

        return article_body.get_text(strip=True) if article_body else ""
    except:
        return ""
