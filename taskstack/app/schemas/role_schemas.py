"""Role schema definitions."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class RoleBase(BaseModel):
    """Base schema for role data."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class RoleResponse(RoleBase):
    """Schema for role responses."""
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
