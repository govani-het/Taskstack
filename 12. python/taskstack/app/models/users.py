
import uuid

from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import ModelColumns


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = ModelColumns.created_at(nullable=False)
    updated_at = ModelColumns.updated_at(nullable=True)
    deleted_at = ModelColumns.deleted_at(nullable=True)

    created_by = ModelColumns.created_by_user(nullable=True)
    updated_by = ModelColumns.updated_by_user(nullable=True)
    deleted_by = ModelColumns.deleted_by_user(nullable=True)

    role = relationship("Role", back_populates="users")
    organization = relationship("Organization",back_populates="users",foreign_keys=[organization_id])

    created_by_user = relationship("User", remote_side=[id], foreign_keys=[created_by])
    updated_by_user = relationship("User", remote_side=[id], foreign_keys=[updated_by])
    deleted_by_user = relationship("User", remote_side=[id], foreign_keys=[deleted_by])
    project_memberships = relationship(
        "ProjectMember", back_populates="user", foreign_keys="ProjectMember.user_id"
    )
