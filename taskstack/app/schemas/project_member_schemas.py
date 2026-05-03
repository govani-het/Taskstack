"""Project member schema definitions."""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.user_schemas import RoleInfo, UserBase



class ProjectMemberBase(BaseModel):
    """Base schema for project member data."""
    user_id: UUID
    role_id: UUID
    project_manager_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class ProjectMemberResponse(ProjectMemberBase):
    """Schema for project member responses."""
    id: UUID
    role: Optional[RoleInfo] = None
    user: Optional[UserBase] = None
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    is_active: bool
    created_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UUID] = None

    class Config:
        from_attributes = True

class RemoveProjectMember(BaseModel):
    """Base schema for project member data."""
    user_id: UUID

    class Config:
        from_attributes = True

class UpdateProjectMemberRole(BaseModel):
    """Schema for updating project member role."""
    role_id: UUID

    class Config:
        from_attributes = True
