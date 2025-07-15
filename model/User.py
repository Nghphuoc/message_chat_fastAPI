import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconfig.config import Base
from sqlalchemy.types import Enum as SqlEnum

class TypeFlag(enum.Enum):
    NOT_ACTIVE = 0
    ACTIVE = 1
    DELETE = 2


class Users(Base):
    __tablename__ = 'TB_USERS'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False, unique=True)
    img_url = Column(String(2048), nullable=False)
    display_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow, nullable=False)
    # delete is 0 active is 1 and other
    flagDelete = Column(SqlEnum(TypeFlag), nullable=False, default=TypeFlag.NOT_ACTIVE)

    role = relationship('Role', back_populates="user") # name class name table
    role_id = Column(String(36), ForeignKey("TB_ROLES.role_id")) # many to one

    status = relationship('UserStatus', back_populates="user", uselist=False) # one to one (uselist=False)

    message = relationship('Message', back_populates="user", uselist=False) # one to one

    sent_friend_requests = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user")
    received_friend_requests = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend")

    reactions = relationship("Reaction", back_populates="user")