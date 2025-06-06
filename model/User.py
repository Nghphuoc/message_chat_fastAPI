import uuid
from datetime import datetime  # ✅ Correct
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dbconfig.config import Base



class Users(Base):
    __tablename__ = 'TB_USERS'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False, unique=True)
    img_url = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow, nullable=False)

    role = relationship('Role', back_populates="user") # name class name table
    role_id = Column(String(36), ForeignKey("TB_ROLES.role_id")) # many to one

    status = relationship('UserStatus', back_populates="user", uselist=False) # one to one (uselist=False)

    message = relationship('Message', back_populates="user", uselist=False) # one to one

    sent_friend_requests = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user")
    received_friend_requests = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend")



