"""Project ORM model."""

import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, UUID
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import TimestampOptionalMixin, UserAuditMixin


class Project(TimestampOptionalMixin, UserAuditMixin, Base):
    """Represents a project record."""
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    organization = relationship("Organization", back_populates="projects")
    created_by_user = relationship("User", foreign_keys="Project.created_by")
    updated_by_user = relationship("User", foreign_keys="Project.updated_by")
    deleted_by_user = relationship("User", foreign_keys="Project.deleted_by")
    members = relationship("ProjectMember", back_populates="project")
    tickets = relationship("Ticket", back_populates="project")
