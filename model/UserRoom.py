import datetime as datetime
import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from dbconfig.config import Base


class UserRoom(Base):
    __tablename__ = 'TB_USER_ROOM'

    user_room_id =  Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_id = Column(String(36), ForeignKey("TB_USERS.user_id"))
    room_id = Column(String(36), ForeignKey("TB_CHAT_ROOMS.chat_room_id"))
    joined_at = Column(DateTime, default = datetime.datetime.now())
    is_active = Column(Boolean, default=True)
    last_read_at = Column(DateTime, nullable = False)
