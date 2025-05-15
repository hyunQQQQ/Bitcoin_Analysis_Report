import requests
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from services.market import get_price

async def send_realtime_price(websocket: WebSocket, interval_sec: int = 2):
    """
    WebSocket을 통해 실시간 비트코인 가격 전송
    - interval_sec: 전송 간격(초)
    """
    await websocket.accept()
    try:
        while True:
            price_data = get_price()
            await websocket.send_json({
                "price": price_data["price"],
                "timestamp": price_data.get("timestamp", None)  # timestamp는 옵션
            })
            await asyncio.sleep(interval_sec)
    except WebSocketDisconnect:
        print("WebSocket 연결 종료됨")
