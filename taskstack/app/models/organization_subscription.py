"""OrganizationSubscription ORM model."""

import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import TimestampOptionalMixin, UserAuditMixin


class OrganizationSubscription(TimestampOptionalMixin, UserAuditMixin, Base):
    """Represents an organization subscription record."""
    __tablename__ = "organization_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    organization = relationship("Organization", back_populates="subscriptions")
    subscription = relationship("Subscription")
    cancelled_by_user = relationship("User", foreign_keys=[cancelled_by])

    __table_args__ = (
        {"schema": None}
    )