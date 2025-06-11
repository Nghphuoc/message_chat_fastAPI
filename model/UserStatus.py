import datetime
import uuid
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from dbconfig.config import Base


class UserStatus(Base):
    __tablename__ = 'TB_USER_STATUS'

    user_status_id = Column(String(36), primary_key = True, default = lambda: str(uuid.uuid4()), nullable = False)
    is_online = Column(Boolean, nullable = False)
    last_seen = Column(DateTime, nullable = False, default = datetime.datetime.now())

    user_id = Column(String(36), ForeignKey('TB_USERS.user_id'), nullable = False)
    user = relationship("Users", back_populates="status") # name class and colum on class