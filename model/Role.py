import enum
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum  # đổi tên để tránh nhầm với Python Enum
from dbconfig.config import Base


class RoleType(enum.Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"

class Role(Base):
    __tablename__ = 'TB_ROLES'

    role_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    role = Column(SqlEnum(RoleType), default = RoleType.MODERATOR, nullable=False)

    user = relationship("Users", back_populates="role")