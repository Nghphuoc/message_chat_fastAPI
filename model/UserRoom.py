import datetime as datetime
import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from dbconfig.config import Base


class UserRoom(Base):
    __tablename__ = 'user_room'

    user_room_id =  Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_id = Column(String(36), ForeignKey("TB_USERS.user_id"), nullable=False)
    room_id = Column(String(36), ForeignKey("TB_CHAT_ROOMS.chat_room_id"), nullable=False)
    joined_at = Column(DateTime, default = datetime.datetime.now())
