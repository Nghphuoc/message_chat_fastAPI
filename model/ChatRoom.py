import datetime as datetime
import uuid
from sqlalchemy import String, Column, DateTime, Boolean
from sqlalchemy.orm import relationship

from dbconfig.config import Base


class ChatRoom(Base):
    __tablename__ = 'TB_CHAT_ROOMS'

    chat_room_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String(255), nullable=False)
    is_group = Column(Boolean, nullable=False, default=False) # check group
    created_at = Column(DateTime, default = datetime.datetime.now(), nullable=False)
    created_by = Column(String(36), nullable=False)

    messages = relationship("Message", back_populates="room")  # đổi tên thuộc tính thành "messages"

