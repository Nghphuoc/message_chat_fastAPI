import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconfig.config import Base


class Message(Base):
    __tablename__ = 'TB_MESSAGES'

    message_id = Column(String(36), primary_key = True, default = lambda: str(uuid.uuid4()), nullable = False)
    content = Column(Text)
    file_url = Column(Text)
    created_at = Column(DateTime, default = datetime.datetime.now(), nullable = False)

    room = relationship("ChatRoom", back_populates="messages")  # đổi "message" → "messages"
    room_id = Column(String(36), ForeignKey("TB_CHAT_ROOMS.chat_room_id"))

    user = relationship("Users", back_populates="message")
    user_id = Column(String(36), ForeignKey("TB_USERS.user_id")) #

