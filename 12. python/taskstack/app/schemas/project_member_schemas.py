from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class RoleInfo(BaseModel):
    name: str


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str


class ProjectMemberBase(BaseModel):
    project_id: UUID
    user_id: UUID
    role_id: UUID
    project_manager_id: Optional[UUID] = None


class ProjectMemberResponse(ProjectMemberBase):
    id: UUID
    role: Optional[RoleInfo] = None
    user: Optional[UserInfo] = None
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True