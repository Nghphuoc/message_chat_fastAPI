from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, EmailStr

from model.Friendship import TypeStatus
from model.Role import RoleType
from model.User import TypeFlag


#Role
class RoleResponse(BaseModel):
    role_id: str
    role_name: RoleType
    create_time: Optional[datetime]
    class Config:
        orm_mode = True

class RoleRequest(BaseModel):
    role_name: RoleType
    create_time: Optional[datetime]
    class Config:
        orm_mode = True


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
        from_attributes = True

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
    class Config:
        orm_mode = True


#UserStatus
class UserStatusRequest(BaseModel):
    is_online: bool
    last_seen: datetime

class UserStatusResponse(BaseModel):
    user_status_id: str
    is_online: bool
    last_seen: datetime
    user: UserResponse
    class Config:
        from_attributes = True


# ChatRoom
class ChatRoomRequest(BaseModel):
    name: str
    is_group: bool
    created_at: datetime
    created_by: UserStatusRequest


class ChatRoomResponse(BaseModel):
    chat_room_id: str
    name: str
    is_group: bool
    created_at: datetime
    created_by: UserStatusRequest

    class Config:
        from_attributes = True


#Message
class MessageRequest(BaseModel):
    content: str
    file_url: str
    created_at: datetime
    room: str
    user: str

class MessageResponse(BaseModel):
    message_id: str
    content: str
    file_url: str
    created_at: datetime
    room: ChatRoomResponse
    user: UserStatusRequest
    class Config:
        from_attributes = True


#Friend
class FriendRequest(BaseModel):
    status: TypeStatus
    created_at: datetime
    friend_id: str # id user connect
    user_id: str

class FriendResponse(BaseModel):
    friend_id: str
    status: TypeStatus
    created_at: datetime
    friend: FriendRequest
    class Config:
        from_attributes = True