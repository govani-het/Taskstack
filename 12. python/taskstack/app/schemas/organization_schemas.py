from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subscription_plan_id: Optional[UUID] = None


class OrganizationCreate(OrganizationBase):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    subscription_plan_id: Optional[UUID] = None
    is_approved: Optional[bool] = None


class OrganizationResponse(OrganizationBase):
    id: UUID
    is_approved: bool
    subscribe_at: Optional[datetime] = None
    cancel_subscription_at: Optional[datetime] = None
    cancel_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True
