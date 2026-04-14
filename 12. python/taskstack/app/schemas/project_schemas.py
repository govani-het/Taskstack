from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class OrganizationInfo(BaseModel):
    name: str


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    organization_id: UUID


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    organization_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: UUID
    is_active: bool
    organization: Optional[OrganizationInfo] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True