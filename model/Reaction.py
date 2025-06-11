import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from dbconfig.config import Base

class Reaction(Base):
    __tablename__ = 'TB_REACTION'

    reaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('TB_USERS.user_id'), nullable=False)
    message_id = Column(String(36), ForeignKey('TB_MESSAGES.message_id'), nullable=False)
    emoji = Column(String(10), nullable=False, default="❤️")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users", back_populates="reactions")
    message = relationship("Message", back_populates="reactions")