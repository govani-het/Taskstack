"""Organization ORM model."""

import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import TimestampOptionalMixin, UserAuditMixin


class Organization(TimestampOptionalMixin, UserAuditMixin, Base):
    """Represents an organization record."""
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    subscription_plan_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True)
    subscribe_at = Column(DateTime(timezone=True), nullable=True)

    cancel_subscription_at = Column(DateTime(timezone=True), nullable=True)
    cancel_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    users = relationship("User",back_populates="organization",foreign_keys="User.organization_id",
    )
    projects = relationship("Project", back_populates="organization")
    subscription_plan = relationship("Subscription", back_populates="organizations")

    created_by_user = relationship("User", foreign_keys="Organization.created_by")
    updated_by_user = relationship("User", foreign_keys="Organization.updated_by")
    deleted_by_user = relationship("User", foreign_keys="Organization.deleted_by")
    cancel_by_user = relationship("User", foreign_keys=[cancel_by])
