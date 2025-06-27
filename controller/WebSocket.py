import datetime
import json
from cachetools import TTLCache
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import asyncio
from model.schema import MessageRequest, UserResponse, UserInRoomResponse
from redis.redis_manager import RedisPubSub
from depends.dependecy import user_status_service, message_service, user_service, user_room_service, reaction_service
from service import StatusService, MessageService, UserRoomService, ReactionService
import logging
from service.webSocketService import WebsocketService

from service.MessageService import to_vietnam_time
from service.UserService import UserService

logger = logging.getLogger(__name__)

ws_router = APIRouter(prefix="/api/ws", tags=["User"])

redis = RedisPubSub()

# { room_id: set of websockets }
connected_clients = {}

@ws_router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str,
                             service_reaction: ReactionService = Depends(reaction_service),
                             service_message: MessageService = Depends(message_service),
                             status_service: StatusService = Depends(user_status_service),
                             service_user: UserService = Depends(user_service)):

    # set cache
    user_cache = TTLCache(maxsize=500, ttl=300)  # save max 500 user, sống 5 minute
    async def get_user_info(data) -> UserResponse:
        if data in user_cache:
            return user_cache[data]
        data_user = service_user.get_user_by_id(data)
        user_cache[data] = data_user
        return data_user

    # step 1: connect websocket
    await websocket.accept()
    status_service.update_status(user_id = user_id, is_online = True)  # online
    # step 2: connect to room
    if room_id not in connected_clients:
        connected_clients[room_id] = set()
    connected_clients[room_id].add(websocket)
    pubsub = await redis.subscribe(room_id)
    print("LOG PUBSUB: ", pubsub)

    # call redis websocket
    async def receive_ws():
        try:
            ws_service = WebsocketService()
            while True:
                raw = await websocket.receive_text()
                payload = json.loads(raw)

                type = payload["type"]
                data = payload["data"]

                if type == "message":
                    try:
                        message = await ws_service.send_message(data, user_id, room_id, service_message, service_user)
                        await redis.publish(room_id, json.dumps(message))
                    except Exception as e:
                        error_payload = {
                            "type": "error",
                            "data": {
                                "message": f"Lỗi xử lý message: {str(e)}"
                            }
                        }
                        await websocket.send_text(json.dumps(error_payload))

                elif type == "reaction":
                    try:
                        # user_id: str
                        #     message_id: str
                        #     emoji: str
                        #     created_at: Optional[datetime]
                        reaction = await service_reaction.create_reaction_and_update(data)
                        reaction_payload = {
                            "type": "reaction",
                            "data": reaction
                        }
                        await redis.publish(room_id,json.dumps(reaction_payload))
                    except Exception as e:
                        error_payload = {
                            "type": "error",
                            "data": {
                                "message": f"Lỗi xử lý reaction: {str(e)}"
                            }
                        }
                        await websocket.send_text(json.dumps(error_payload))
                        continue

        except WebSocketDisconnect:
            pass
        finally:
            # Xóa client khi disconnect
            status_service.update_status(user_id=user_id, is_online=False)  # online
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                # Nếu phòng không còn ai, hủy subscribe hoặc xóa key
                connected_clients.pop(room_id, None)


    async def send_ws():
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if message:
                    try:
                        payload = json.loads(message["data"])
                        sender_id = payload.get("data", {}).get("user_id")

                        # Gửi message đến các client khác trong phòng
                        for client in connected_clients.get(room_id, []):
                            if hasattr(client, "user_id") and client.user_id == sender_id:
                                continue  # next user send message
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


@ws_router.websocket("/status/{user_id}")
async def user_ws(websocket: WebSocket, user_id: str,
                  status_service: StatusService = Depends(user_status_service)):
    await websocket.accept()
    print(f"[STATUS] Set user {user_id} online")  # DEBUG
    status_service.update_status(user_id, True) # online
    try:
        while True:
            # Giữ kết nối
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        status_service.update_status(user_id, False) # offline
