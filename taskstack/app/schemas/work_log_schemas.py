"""Work log schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


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
    created_at: str
    updated_at: str
    created_by: UUID
    updated_by: UUID

    class Config:
        from_attributes = True