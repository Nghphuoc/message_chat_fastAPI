import datetime
import uuid
import enum
from enum import unique

from sqlalchemy import String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from dbconfig.config import Base
from sqlalchemy.types import Enum as SqlEnum


class TypeStatus(enum.Enum):
    PENDING = "PENDING"
    WAIT = "WAIT"
    ACCEPTED = "ACCEPTED"
    BLOCKED = "BLOCKED"


class Friendship(Base):
    __tablename__ = 'TB_FRIENDSHIPS'

    friendship_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    status = Column(SqlEnum(TypeStatus), nullable=False)  # pending, accepted
    created_at = Column(DateTime, default = datetime.datetime.now())

    friend_id = Column(String(36), ForeignKey('TB_USERS.user_id'), nullable=False)
    user_id = Column(String(36), ForeignKey('TB_USERS.user_id'), nullable=False) # , nullable=False

    user = relationship("Users", foreign_keys=[user_id], back_populates="sent_friend_requests")
    friend = relationship("Users", foreign_keys=[friend_id], back_populates="received_friend_requests")
