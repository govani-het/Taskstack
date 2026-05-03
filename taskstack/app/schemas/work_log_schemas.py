"""Work log schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class WorkLogBase(BaseModel):
    """Base work log schema."""
    description: Optional[str] = Field(None, max_length=1000)
    time_spent_minutes: int = Field(..., gt=0)


class WorkLogCreate(WorkLogBase):
    """Work log creation schema."""
    project_id: UUID
    ticket_id: UUID


class WorkLogUpdate(BaseModel):
    """Work log update schema."""
    description: Optional[str] = Field(None, max_length=1000)
    time_spent_minutes: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class WorkLogResponse(WorkLogBase):
    """Work log response schema."""
    id: UUID
    project_id: UUID
    ticket_id: UUID
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: UUID
    updated_by: Optional[UUID] = None
    deleted_by: Optional[UUID] = None

    class Config:
        from_attributes = True
