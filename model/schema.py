from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import relationship
from datetime import datetime
from dbconfig.config import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class UserStatus(Base):
    __tablename__ = "tb_user_status"

    user_status_id = Column(String, primary_key=True)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime)

    users = relationship("User", back_populates="status")


class Role(Base):
    __tablename__ = "tb_roles"

    role_id = Column(String, primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "tb_users"

    user_id = Column(String, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    display_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    role_id = Column(String, ForeignKey("tb_roles.role_id"))
    status_id = Column(String, ForeignKey("tb_user_status.user_status_id"))

    role = relationship("Role", back_populates="users")
    status = relationship("UserStatus", back_populates="users")

    messages = relationship("Message", back_populates="user")
    friendships = relationship("Friendship", back_populates="user", foreign_keys='Friendship.user_id')
    friend_of = relationship("Friendship", back_populates="friend", foreign_keys='Friendship.friend_id')
    rooms = relationship("UserRoom", back_populates="user")


class Friendship(Base):
    __tablename__ = "tb_friendships"

    friendship_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("tb_users.user_id"))
    friend_id = Column(String, ForeignKey("tb_users.user_id"))
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="friendships")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friend_of")


class ChatRoom(Base):
    __tablename__ = "tb_chat_rooms"

    chat_room_id = Column(String, primary_key=True)
    name = Column(String)
    is_group = Column(Boolean, default=False)
    created_by = Column(String, ForeignKey("tb_users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="room")
    participants = relationship("UserRoom", back_populates="room")


class UserRoom(Base):
    __tablename__ = "user_room"

    user_room_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("tb_users.user_id"))
    room_id = Column(String, ForeignKey("tb_chat_rooms.chat_room_id"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rooms")
    room = relationship("ChatRoom", back_populates="participants")


class Message(Base):
    __tablename__ = "tb_messages"

    message_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("tb_users.user_id"))
    room_id = Column(String, ForeignKey("tb_chat_rooms.chat_room_id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    room = relationship("ChatRoom", back_populates="messages")
