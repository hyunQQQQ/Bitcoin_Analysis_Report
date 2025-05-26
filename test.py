import os
from dotenv import load_dotenv

# 이 경로는 반드시 루트 기준
load_dotenv(dotenv_path=".env")

print("✅ TEST - NAVER_CLIENT_ID:", os.getenv("NAVER_CLIENT_ID"))
print("✅ TEST - NAVER_CLIENT_SECRET:", os.getenv("NAVER_CLIENT_SECRET"))
