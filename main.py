from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from starlette.middleware.cors import CORSMiddleware
from dbconfig.config import Base, engine
from redis.redis_manager import RedisPubSub
import model.User
import model.Role
import model.Friendship
import model.ChatRoom
import model.UserRoom
import model.UserStatus
import model.Messages

app = FastAPI()
redis = RedisPubSub()

# Lưu client theo phòng
connected_clients = {}  # { room_id: set of websockets }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await redis.connect()
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created.")


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()

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
