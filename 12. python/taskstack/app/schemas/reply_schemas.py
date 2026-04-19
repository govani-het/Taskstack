"""Reply schema definitions."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ReplyBase(BaseModel):
    reply: str = Field(..., min_length=1, max_length=1000)

    class Config:
        from_attributes = True


class ReplyCreate(ReplyBase):
    pass


class ReplyUpdate(ReplyBase):
    pass


class ReplyResponse(ReplyBase):
    id: UUID
    comment_id: UUID
    project_id: UUID
    created_by: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True