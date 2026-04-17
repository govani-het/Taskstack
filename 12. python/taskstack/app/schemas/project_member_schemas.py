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

    class Config:
        from_attributes = True
