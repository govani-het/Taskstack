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


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    plan_name: Optional[str] = Field(None, min_length=1, max_length=100)
    validity: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription responses."""
    id: UUID

    class Config:
        from_attributes = True


class SubscriptionBasicResponse(BaseModel):
    """Schema for subscription basic responses."""
    id: UUID
    plan_name: str

    class Config:
        from_attributes = True
