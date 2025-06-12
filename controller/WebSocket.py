from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import asyncio

from depends.dependecy import user_status_service
from redis.redis_manager import RedisPubSub
from service import StatusService

ws_router = APIRouter = APIRouter(prefix="/api/ws", tags=["User"])
redis = RedisPubSub()


# Lưu client theo phòng
connected_clients = {}  # { room_id: set of websockets }

@ws_router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str, service: StatusService = Depends(user_status_service)):

    await websocket.accept()
    # set 👉 online status for user
    service.update_status(user_id, True)

    if room_id not in connected_clients:
        connected_clients[room_id] = set()
    connected_clients[room_id].add(websocket)
    pubsub = await redis.subscribe(room_id)

    async def receive_ws():
        try:
            while True:
                data = await websocket.receive_text()
                await redis.publish(room_id, data)
        except WebSocketDisconnect:
            pass
        finally:
            # Xóa client khi disconnect
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                # Nếu phòng không còn ai, hủy subscribe hoặc xóa key
                connected_clients.pop(room_id, None)
                service.update_status(user_id, False)  # 👉 OFFLINE


    async def send_ws():
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if message:
                    # Gửi message cho client trong đúng phòng
                    for client in connected_clients.get(room_id, []):
                        if client.client_state.value == 1:  # CONNECTED
                            await client.send_text(message['data'])
        except WebSocketDisconnect:
            # Nếu send_ws bị disconnect, cũng xóa client
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                connected_clients.pop(room_id, None)

    await asyncio.gather(receive_ws(), send_ws())
