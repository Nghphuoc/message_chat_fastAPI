from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, EmailStr

from model import UserStatus
from model.Friendship import TypeStatus
from model.Role import RoleType
from model.User import TypeFlag


#Role
class RoleResponse(BaseModel):
    role_id: str
    role_name: RoleType
    create_time: Optional[datetime]
    class Config:
        orm_mode = True  # Dành cho Pydantic v1

class RoleRequest(BaseModel):
    role_name: RoleType
    create_time: Optional[datetime]
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


#User
class UserRequest(BaseModel):
    username: constr(min_length=3, max_length=64)
    password: constr(min_length=8, max_length=64)
    email: EmailStr
    phone: constr(regex=r"^0\d{9}$")
    img_url: Optional[str] = None
    display_name: Optional[constr(min_length=3, max_length=64)] = None
    created_at: datetime
    role_id: Optional[str] = None
    flagDelete: Optional[TypeFlag]
    class Config:
        orm_mode = True  # Dành cho Pydantic v1

class UserResponse(BaseModel):
    user_id: str
    username: str
    password: str
    email: str
    phone: str
    img_url: str
    display_name: str
    created_at: datetime
    role: Optional[RoleResponse]
    flagDelete: Optional[TypeFlag]
    #status: UserStatusResponse
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


#UserStatus
class UserStatusRequest(BaseModel):
    is_online: bool
    last_seen: datetime

class UserStatusResponse(BaseModel):
    user_status_id: str
    is_online: bool
    last_seen: datetime
    user_id: str
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


# ChatRoom
class ChatRoomRequest(BaseModel):
    name: Optional[str]
    is_group: bool
    created_at: Optional[datetime]
    created_by: str
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


class ChatRoomResponse(BaseModel):
    chat_room_id: str
    name: Optional[str]
    is_group: bool
    created_at: datetime
    created_by: Optional[str]
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


#Message
class MessageRequest(BaseModel):
    content: str
    file_url: Optional[str]
    created_at: Optional[datetime]
    room: str
    user: str

class MessageResponse(BaseModel):
    message_id: str
    content: str
    file_url: Optional[str]
    created_at: Optional[datetime]
    room: ChatRoomResponse
    user: UserResponse
    class Config:
        orm_mode = True  # Dành cho Pydantic v1

#Friend
class FriendRequest(BaseModel):
    status: TypeStatus
    created_at: Optional[datetime]
    friend_id: str # id user connect
    user_id: str

class FriendResponse(BaseModel):
    friend_id: str
    status: TypeStatus
    created_at: datetime
    friend_id: str  # id user connect
    user_id: str
    class Config:
        orm_mode = True  # Dành cho Pydantic v1


# UserRoom
class UserRoomRequest(BaseModel):
    user_id: str
    room_id: str
    joined_at: Optional[datetime]
    class Config:
        orm_mode = True

class UserRoomResponse(BaseModel):
    user_room_id: Optional[str]
    user_id: Optional[str]
    room_id: Optional[str]
    joined_at: Optional[datetime]
    class Config:
        orm_mode = True


# Reaction
class ReactionRequest(BaseModel):
    user_id: str
    message_id: str
    emoji: str
    created_at: Optional[datetime]

class ReactionResponse(BaseModel):
    reaction_id: str
    message_id: str
    emoji: str
    created_at: Optional[datetime]
    class Config:
        orm_mode = True


class UserInRoomResponse(BaseModel):
    img_url: str
    username: str
    room_id: str
    status: bool
    last_seen: Optional[datetime]
    class Config:
        orm_mode = True


#Login
class LoginRequest(BaseModel):
    username: str
    password: str


#Token
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None