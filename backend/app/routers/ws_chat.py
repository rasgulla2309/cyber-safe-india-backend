from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

# user_id → websocket
active_connections: Dict[int, WebSocket] = {}


@router.websocket("/ws/chat/{user_id}")
async def chat_socket(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            # broadcast to admin (simple version)
            for uid, ws in active_connections.items():
                await ws.send_text(f"{user_id}:{data}")

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
