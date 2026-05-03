"""User schema definitions."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class RoleInfo(BaseModel):
    """Compact schema for role information."""
    name: str

    class Config:
        from_attributes = True

class OrganizationInfo(BaseModel):
    """Compact schema for organization information."""
    name: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    """Base schema for user data."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=100)
    role_name: str
    organization_name: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for updating a user."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role_name: Optional[str] = None
    organization_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    """Schema for user responses."""
    id: UUID
    role: Optional[RoleInfo] = None
    organization: Optional[OrganizationInfo] = None
    is_active: bool

    class Config:
        from_attributes = True