"""OrganizationSubscription schema definitions."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class OrganizationSubscriptionBase(BaseModel):
    """Base schema for organization subscription data."""
    subscription_id: UUID = Field(..., description="Subscription plan ID")


class OrganizationSubscriptionCreate(OrganizationSubscriptionBase):
    """Schema for creating an organization subscription."""
    pass


class OrganizationSubscriptionResponse(BaseModel):
    """Schema for organization subscription responses."""
    id: UUID
    organization_id: UUID
    subscription_id: UUID
    subscribed_at: datetime
    cancelled_at: Optional[datetime]
    cancelled_by: Optional[UUID]
    is_active: bool
    created_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UUID] = None

    class Config:
        from_attributes = True


class OrganizationSubscriptionBasicResponse(BaseModel):
    """Schema for organization subscription basic responses."""
    id: UUID
    subscription_id: UUID
    subscribed_at: datetime
    is_active: bool
    created_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UUID] = None

    class Config:
        from_attributes = True
