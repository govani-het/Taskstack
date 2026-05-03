"""Subscription schema definitions."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class SubscriptionBase(BaseModel):
    """Base schema for subscription data."""
    plan_name: str = Field(..., min_length=1, max_length=100)
    validity: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    allowed_projects: float = Field(default=5, ge=1)


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    plan_name: Optional[str] = Field(None, min_length=1, max_length=100)
    validity: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    allowed_projects: Optional[float] = Field(None, ge=1)


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription responses."""
    id: UUID
    is_active: bool
    created_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UUID] = None

    class Config:
        from_attributes = True


class SubscriptionBasicResponse(BaseModel):
    """Schema for subscription basic responses."""
    id: UUID
    plan_name: str

    class Config:
        from_attributes = True
