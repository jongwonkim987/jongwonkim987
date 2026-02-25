"""
마켓 라우터 (Market Layer)
- WebSocket을 통한 실시간 시세 브로드캐스트 및 시세 생성
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, random, datetime

router = APIRouter()


class ConnectionManager:
    """웹소켓 연결 관리자"""
    def __init__(self):
        # 연결된 클라이언트 리스트 저장
        self.active_connections = []

    async def connect(self, ws: WebSocket):
        # TODO: 웹소켓 연결을 수락(accept)하고 리스트에 추가하세요
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # TODO: 리스트에서 웹소켓 연결을 제거하세요
        self.active_connections.remove(ws)

    async def broadcast(self, msg: dict):
        # TODO: 연결된 모든 클라이언트에게 JSON 형식의 메시지를 전송하세요
        for conn in self.active_connections:
            try:
                await conn.send_json(msg)
            except Exception:
                self.active_connections.remove(conn)


manager = ConnectionManager()


async def price_generator():
    price = 50000
    while True:
        price += random.randint(-600, 600)
        price = max(1000, price)

        await manager.broadcast(
            {
                "type": "price_update",
                "price": int(price),
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
            }
        )
        await asyncio.sleep(1.5)


@router.websocket("/ws/market")
async def websocket_endpoint(ws: WebSocket):
    """웹소켓 엔드포인트"""
    # TODO: manager를 통해 클라이언트를 연결하세요
    # TODO: 클라이언트가 연결을 끊을 때까지 대기하고, 종료 시 disconnect 처리하세요
    await manager.connect(ws)

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
