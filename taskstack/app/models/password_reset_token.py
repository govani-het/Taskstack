"""Password reset token ORM model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, func

from app.config.database import Base
from app.models.model_columns import TimestampRequiredMixin, UserAuditMixin


class PasswordResetToken(TimestampRequiredMixin, UserAuditMixin, Base):
    """Represents a password reset token record."""
    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token = Column(String(32), nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def is_expired(self) -> bool:
        """Check if the token has expired."""
        return datetime.now(timezone.utc) > self.expires_at

    def is_valid(self) -> bool:
        """Check if the token is valid (not used and not expired)."""
        return not self.used and not self.is_expired()
