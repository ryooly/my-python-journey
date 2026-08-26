from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from parents.auth.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(512), unique=True, nullable=False, index=True)
    is_revoked = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
