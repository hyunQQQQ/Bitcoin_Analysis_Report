import requests
from bs4 import BeautifulSoup
import html
import os
from dotenv import load_dotenv

# 네이버 API 인증 정보
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def get_naver_news_api(query="비트코인", limit=10):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=100"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    print(f"\n[뉴스 API 호출] 키워드: {query}")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        ###print("응답 코드:", response.status_code)

        response.raise_for_status()
        items = response.json().get('items', [])
        ###print("응답 뉴스 수:", len(items))
    except Exception as e:
        print("뉴스 API 호출 실패:", e)
        return []

    news_list = []
    for item in items:
        link = item.get('link', '')
        if "n.news.naver.com" in link:
            title_unescaped = html.unescape(item.get('title', ''))
            title_clean = BeautifulSoup(title_unescaped, "html.parser").get_text()
            news_list.append({
                "title": title_clean,
                "url": link
            })
            

            if len(news_list) >= limit:
                break

    print("📄 최종 뉴스 반환 수:", len(news_list))
    return news_list

def get_article_content(url):
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
