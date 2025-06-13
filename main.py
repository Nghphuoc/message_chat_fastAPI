from fastapi import FastAPI
from controller.RoleController import router as role_router
from controller.UserController import router as user_router
from starlette.middleware.cors import CORSMiddleware
from dbconfig.config import Base, engine
from controller.WebSocket import redis  # chỉ import redis
from controller.WebSocket import ws_router
from controller.RoomController import router as room_router
from controller.UserRoomController import router as user_room_router
from controller.UserAndFriendCreateController import router as user_friend_create_router
from controller.FriendController import router as friend_router
from model.Reaction import Reaction
from model.ChatRoom import ChatRoom
from model.Friendship import Friendship
from model.Messages import Message
from model.Role import Role
from model.User import Users
from model.UserRoom import UserRoom
from model.UserStatus import UserStatus
import model

from dbconfig import config
print("Database URL:", config.DATABASE_URL)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(room_router)
app.include_router(user_room_router)
app.include_router(user_friend_create_router)
app.include_router(friend_router)

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    await redis.connect()
    print("Creating tables...")
    print("Tables created.")

