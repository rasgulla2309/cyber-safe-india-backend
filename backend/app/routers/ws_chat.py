from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

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

            message_data = json.loads(data)

            # broadcast to all connected clients
            for uid, ws in active_connections.items():
                await ws.send_text(json.dumps({
                    "sender": message_data["sender"],
                    "message": message_data["message"],
                    "user_id": user_id
                }))

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
