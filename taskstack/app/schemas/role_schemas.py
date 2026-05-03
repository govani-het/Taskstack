"""Role schema definitions."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


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

    class Config:
        from_attributes = True
