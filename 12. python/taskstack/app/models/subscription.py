"""Subscription ORM model."""

import uuid

from sqlalchemy import UUID, Column, Float, String, Boolean
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import TimestampOptionalMixin, UserAuditMixin


class Subscription(TimestampOptionalMixin, UserAuditMixin, Base):
    """Represents a subscription record."""
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    plan_name = Column(String(100), nullable=False, unique=True)
    validity = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    organizations = relationship("Organization", back_populates="subscription_plan")
