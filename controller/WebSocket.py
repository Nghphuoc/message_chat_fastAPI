import datetime
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import asyncio
from model.schema import MessageRequest
from redis.redis_manager import RedisPubSub
from depends.dependecy import user_status_service, message_service
from service import StatusService, MessageService
import logging

logger = logging.getLogger(__name__)

ws_router = APIRouter(prefix="/api/ws", tags=["User"])

redis = RedisPubSub()


# Lưu client theo phòng
connected_clients = {}  # { room_id: set of websockets }

@ws_router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str,
                             service: StatusService = Depends(user_status_service),
                             service_message: MessageService = Depends(message_service)):

    await websocket.accept()
    #connected_clients[user_id] = websocket
    # step 1: set 👉 online status for user or ) create new if don't have
    service.update_status(user_id, True)

    # step 2: connect to room
    if room_id not in connected_clients:
        connected_clients[room_id] = set()
    connected_clients[room_id].add(websocket)
    pubsub = await redis.subscribe(room_id)
    print("LOG PUBSUB: ", pubsub)

    # call redis websocket
    async def receive_ws():
        try:
            while True:
                data = await websocket.receive_text()
                # step 1: update data send in websocket
                data_send = MessageRequest(
                    user=user_id,
                    room=room_id,
                    content=data,
                    file_url="", # optional
                    created_at=datetime.datetime.utcnow(),
                )
                # add to database message
                try:
                    # step 2: insert data message
                    message_data = service_message.insert_message(data_send)
                except Exception as e:
                    raise HTTPException(status_code=500, detail={"message": str(e)})
                await redis.publish(room_id, json.dumps({
                                                        "message_id": message_data.message_id,
                                                        "user_id": user_id,
                                                        "room_id": room_id,
                                                        "content": data,
                                                        "created_at": str(data_send.created_at)}))
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
                    try:
                        payload = json.loads(message["data"])
                        sender_id = payload["user_id"]

                        # Gửi message đến các client khác trong phòng
                        for client in connected_clients.get(room_id, []):
                            if hasattr(client, "user_id") and client.user_id == sender_id:
                                continue  # bỏ qua người gửi
                            if client.client_state.value == 1:  # CONNECTED
                                await client.send_text(message['data'])

                    except Exception as e:
                        logger.error(f"Error processing Redis message: {e}")

        except WebSocketDisconnect:
            # Nếu send_ws bị disconnect, cũng xóa client
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                connected_clients.pop(room_id, None)

    await asyncio.gather(receive_ws(), send_ws())
