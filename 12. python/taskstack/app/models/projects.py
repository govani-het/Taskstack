import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, UUID
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import ModelColumns

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = ModelColumns.created_at(nullable=True)
    updated_at = ModelColumns.updated_at(nullable=True)
    deleted_at = ModelColumns.deleted_at(nullable=True)

    created_by = ModelColumns.created_by_user(nullable=True)
    updated_by = ModelColumns.updated_by_user(nullable=True)
    deleted_by = ModelColumns.deleted_by_user(nullable=True)

    organization = relationship("Organization", back_populates="projects")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    deleted_by_user = relationship("User", foreign_keys=[deleted_by])
    members = relationship("ProjectMember", back_populates="project")
    tickets = relationship("Ticket", back_populates="project")
