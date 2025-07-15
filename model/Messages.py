from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship
from dbconfig.config import Base


class Message(Base):
    __tablename__ = 'TB_MESSAGES'

    message_id = Column(String(36), primary_key = True, default = lambda: str(uuid.uuid4()), nullable = False)
    content = Column(Text)
    file_url = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable = False)
    # is_deleted = Column(NUMBER, default = 0)

    room = relationship("ChatRoom", back_populates="messages")  # đổi "message" → "messages"
    room_id = Column(String(36), ForeignKey("TB_CHAT_ROOMS.chat_room_id"))

    user = relationship("Users", back_populates="message")
    user_id = Column(String(36), ForeignKey("TB_USERS.user_id")) #

    reactions = relationship("Reaction", back_populates="message", cascade="all, delete-orphan")

