from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class RoleInfo(BaseModel):
    name: str

    class Config:
        from_attributes = True

class OrganizationInfo(BaseModel):
    name: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    role_name: str
    organization_name: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role_name: Optional[str] = None
    organization_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    id: UUID
    role: Optional[RoleInfo] = None
    organization: Optional[OrganizationInfo] = None
    is_active: bool

    class Config:
        from_attributes = True