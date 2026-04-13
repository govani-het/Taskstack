import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String(500), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", backref="refresh_tokens")
