import datetime
import json
from cachetools import TTLCache
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import asyncio
from model.schema import MessageRequest, UserResponse, UserInRoomResponse
from redis.redis_manager import RedisPubSub
from depends.dependecy import user_status_service, message_service, user_service, user_room_service
from service import StatusService, MessageService, UserRoomService
import logging

from service.MessageService import to_vietnam_time
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
                service.update_status(user_id=user_id, is_online=False)
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


# # call ws get room and list chat of user
# @ws_router.websocket("/status/{user_id}")
# async def get_all_room_of_user(user_id: str, websocket: WebSocket,
#                                service_user_room: UserRoomService = Depends(user_room_service),
#                                user_service: UserService = Depends(user_service),
#                                user_status: StatusService = Depends(user_status_service)):
#
#     await websocket.accept()
#     user_status.update_status(user_id=user_id, is_online=True)
#     print(f"[ONLINE] User {user_id} is now online.")
#
#     try:
#         while True:
#             room_ids = service_user_room.get_all_list_room_for_user(user_id)
#             result = []
#              # step 1: get room of user
#             for room_tuple in room_ids:
#                 room_id = room_tuple[0]
#                 # step 1.1: call service ( include user_id and friend_id much filed )
#                 user_rooms = service_user_room.get_user_id_by_room_id(room_id)
#                 # step 1.2: get user_id
#                 for user_room in user_rooms:
#                     if str(user_room.user_id) != str(user_id):
#                         user_info = user_service.get_user_by_id(user_room.user_id)
#                         if not user_info:
#                             continue
#
#                         status_user = user_status.get_status_by_user(user_info.user_id)
#                         display_name = user_info.display_name or user_info.username
#                         # step 1.3: add list to return
#                         result.append(UserInRoomResponse(
#                             img_url=user_info.img_url,
#                             username=display_name,
#                             room_id=user_room.room_id,
#                             status=status_user.is_online if status_user else False,
#                             last_seen=to_vietnam_time(status_user.last_seen) if status_user else None,
#                         ))
#
#             # Gửi danh sách phòng cho client mỗi 10 giây
#             await websocket.send_json([r.dict() for r in result])
#             await asyncio.sleep(10)
#
#     except WebSocketDisconnect:
#         print(f"[DISCONNECT] User {user_id} disconnected.")
#         user_status.update_status(user_id=user_id, is_online=False)
#
#     except Exception as e:
#         print(f"[ERROR] WebSocket error for {user_id}: {e}")
#         user_status.update_status(user_id=user_id, is_online=False)
#         await websocket.close()