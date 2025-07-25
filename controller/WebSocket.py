import datetime
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import asyncio
from starlette.websockets import WebSocketState
from redis_client.redis_manager import RedisPubSub
from depends.dependecy import user_status_service, message_service, user_service, user_room_service, reaction_service, room_service
from service import StatusService, MessageService, UserRoomService, ReactionService, RoomService
import logging
from service.webSocketService import WebsocketService
from service.MessageService import to_vietnam_time
from service.UserService import UserService

logger = logging.getLogger(__name__)
ws_router = APIRouter(prefix="/api/ws", tags=["User"])
redis = RedisPubSub()
# { room_id: set of websockets }
connected_clients = {}
# { user_id: websocket }
user_status_sockets = {}

@ws_router.websocket("/status/update/{user_id}")
async def user_ws(websocket: WebSocket, user_id: str,
                  status_service: StatusService = Depends(user_status_service),
                  user_room_service: UserRoomService = Depends(user_room_service)):
    await websocket.accept()

    # Cập nhật status online
    status_service.update_status(user_id=user_id, is_online=True)
    user_status_sockets[user_id] = websocket  # Lưu WebSocket

    try:
        # Gửi thông báo status đến tất cả user trong các phòng chat chung
        rooms = user_room_service.get_all_list_room_for_user(user_id)
        notified_users = set()

        for room in rooms:
            room_id = room[0]
            participants = user_room_service.get_user_id_by_room_id(room_id)
            for participant in participants:
                target_user_id = str(participant.user_id)
                if target_user_id != user_id and target_user_id not in notified_users:
                    notified_users.add(target_user_id)
                    if target_user_id in user_status_sockets:
                        status_payload = {
                            "type": "status",
                            "data": {
                                "user_id": user_id,
                                "is_online": True,
                                "last_seen": str(to_vietnam_time(datetime.datetime.now()))
                            }
                        }
                        await user_status_sockets[target_user_id].send_text(json.dumps(status_payload))

        # Giữ kết nối mở
        while True:
            try:
                await websocket.receive_text()  # Chờ nhận tin nhắn hoặc ngắt kết nối
            except WebSocketDisconnect:
                logger.info(f"User {user_id} disconnected unexpectedly")
                break  # Ra khỏi vòng lặp khi WebSocketDisconnect

            await asyncio.sleep(30)  # Có thể thêm delay trong khi kết nối mở

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        # Cập nhật offline và gửi thông báo
        logger.info(f"User {user_id} offline")
        status_service.update_status(user_id=user_id, is_online=False)
        user_status_sockets.pop(user_id, None)

        # Gửi thông báo offline đến các user liên quan
        rooms = user_room_service.get_all_list_room_for_user(user_id)
        notified_users = set()

        for room in rooms:
            room_id = room[0]
            participants = user_room_service.get_user_id_by_room_id(room_id)
            for participant in participants:
                target_user_id = str(participant.user_id)
                if target_user_id != user_id and target_user_id not in notified_users:
                    notified_users.add(target_user_id)
                    if target_user_id in user_status_sockets:
                        status_payload = {
                            "type": "status",
                            "data": {
                                "user_id": user_id,
                                "is_online": False,
                                "last_seen": str(to_vietnam_time(datetime.datetime.now()))
                            }
                        }
                        await user_status_sockets[target_user_id].send_text(json.dumps(status_payload))


@ws_router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str,
                             service_reaction: ReactionService = Depends(reaction_service),
                             service_message: MessageService = Depends(message_service),
                             status_service: StatusService = Depends(user_status_service),
                             service_user: UserService = Depends(user_service),
                             service_room: RoomService = Depends(room_service)):

    # step 1: connect websocket
    await websocket.accept()
    status_service.update_status(user_id = user_id, is_online = True)  # online
    # step 2: connect to room
    if room_id not in connected_clients:
        connected_clients[room_id] = set()
    connected_clients[room_id].add(websocket)
    pubsub = await redis.subscribe(room_id)
    print("LOG PUBSUB: ", pubsub)

    # call redis_client websocket
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
                        message = await ws_service.send_message(data, user_id, room_id, service_message, service_user, service_room)
                        await redis.publish(room_id, json.dumps(message))
                    except Exception as e:
                        error_payload = {
                            "type": "error",
                            "data": {
                                "message": {str(e)}
                            }
                        }
                        await websocket.send_text(json.dumps(error_payload))

                elif type == "reaction":
                    try:
                        reaction_payload = await ws_service.send_reaction(data, room_id, service_reaction, service_room, service_user)
                        await redis.publish(room_id, json.dumps(reaction_payload))
                    except Exception as e:
                        print("ERROR CREATE REACTION AT ReactionService: ", e)
                        error_payload = {
                            "type": "error",
                            "data": {
                                "message": {str(e)}
                            }
                        }
                        await websocket.send_text(json.dumps(error_payload))

                elif type == "cancel_reaction":
                    try:
                        cancel_reaction = await ws_service.cancel_reaction(data, user_id, service_reaction)
                        await redis.publish(room_id, json.dumps(cancel_reaction))
                    except Exception as e:
                        print("ERROR CANCEL REACTION AT ReactionService: ", e)
                        error_payload = {
                            "type": "error",
                            "data": {
                                "message": {str(e)}
                            }
                        }
                        await websocket.send_text(json.dumps(error_payload))

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

                        dead_clients = set()

                        for client in connected_clients.get(room_id, []):
                            try:
                                if hasattr(client, "user_id") and client.user_id == sender_id:
                                    continue
                                if client.application_state == WebSocketState.CONNECTED:
                                    await client.send_text(message['data'])
                            except Exception as e:
                                logger.warning(f"⚠️ Client send error, removing client: {e}")
                                dead_clients.add(client)

                        # Cleanup dead connections
                        for dead in dead_clients:
                            connected_clients[room_id].discard(dead)

                    except Exception as e:
                        logger.error(f"Error processing Redis message: {e}")

        except WebSocketDisconnect:
            connected_clients[room_id].discard(websocket)
            if not connected_clients[room_id]:
                connected_clients.pop(room_id, None)

    await asyncio.gather(receive_ws(), send_ws())