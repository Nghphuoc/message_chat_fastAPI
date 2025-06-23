import datetime
import json
from cachetools import TTLCache
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import asyncio
from model.schema import MessageRequest, UserResponse
from redis.redis_manager import RedisPubSub
from depends.dependecy import user_status_service, message_service, user_service
from service import StatusService, MessageService
import logging


from service.UserService import UserService

logger = logging.getLogger(__name__)

ws_router = APIRouter(prefix="/api/ws", tags=["User"])

redis = RedisPubSub()


# Lưu client theo phòng
connected_clients = {}  # { room_id: set of websockets }

@ws_router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str,
                             service: StatusService = Depends(user_status_service),
                             service_message: MessageService = Depends(message_service),
                             service_user: UserService = Depends(user_service)):

    # set cache
    user_cache = TTLCache(maxsize=500, ttl=300)  # Lưu tối đa 500 user, sống 5 phút
    async def get_user_info(data) -> UserResponse:
        if data in user_cache:
            return user_cache[data]
        data_user = service_user.get_user_by_id(data)
        user_cache[data] = data_user
        return data_user

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

                # call cache get data user
                data_user = await get_user_info(user_id)
                if data_user.display_name is None:
                    name_user = data_user.username
                else:
                    name_user = data_user.display_name

                await redis.publish(room_id, json.dumps({
                                                        "message_id": message_data.message_id,
                                                        "user_id": user_id,
                                                        "name_user": name_user,
                                                        "img_url": data_user.img_url,
                                                        "room_id": room_id,
                                                        "content": data,
                                                        "created_at": str(MessageService.to_vietnam_time(data_send.created_at))}))
        except WebSocketDisconnect:
            service.update_status(user_id, False)  # 👉 OFFLINE
            pass
        finally:
            # Xóa client khi disconnect
            service.update_status(user_id=user_id, is_online=False)
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                service.update_status(user_id, False)  # 👉 OFFLINE
                # Nếu phòng không còn ai, hủy subscribe hoặc xóa key
                connected_clients.pop(room_id, None)


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
