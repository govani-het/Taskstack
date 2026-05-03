"""Project schema definitions."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.organization_schemas import OrganizationInfo



class ProjectBase(BaseModel):
    """Base schema for project data."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    organization_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class ProjectResponse(ProjectBase):
    """Schema for project responses."""
    id: UUID
    is_active: bool
    organization: Optional[OrganizationInfo] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True
