"""Role ORM model."""

import uuid

from sqlalchemy import UUID, Column, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import TimestampOptionalMixin, UserAuditMixin


class Role(TimestampOptionalMixin, UserAuditMixin, Base):
    """Represents a role record."""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    users = relationship("User", back_populates="role", foreign_keys="User.role_id")
    project_members = relationship("ProjectMember", back_populates="role")
