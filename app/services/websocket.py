import requests
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from services.market import get_price

async def send_realtime_price(websocket: WebSocket, interval_sec: int = 2):
    await websocket.accept()
    try:
        while True:
            price_data = get_price()
            await websocket.send_json({
                "price": price_data["price"],
                "timestamp": price_data.get("timestamp", None)
            })
            await asyncio.sleep(interval_sec)
    except WebSocketDisconnect:
        print("WebSocket 연결 종료됨")
