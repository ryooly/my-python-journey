from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    JSON,
    DateTime,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    token = Column(String(512), unique=True, nullable=False, index=True)
    jti = Column(String(64), unique=True, nullable=True, index=True) 

    device_info = Column(String(255), nullable=True)   # info device/browser
    ip_address = Column(String(45), nullable=True)      # IPv4/IPv6

    is_revoked = Column(Boolean, default=False, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)   # buat token rotation

    extra_data = Column(JSON, nullable=True)  # payload tambahan kalau perlu

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )


