"""Ticket schema definitions."""

from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

TicketType = Literal["bug", "task"]
TicketStatus = Literal["pending", "process", "completed", "canceled"]
TicketPriority = Literal["high", "intermediate", "low"]


class TicketBase(BaseModel):
    """Base schema for ticket payloads."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    type: TicketType = Field(...)
    status: Optional[TicketStatus] = Field(None)
    priority: Optional[TicketPriority] = Field(None)
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketCreate(TicketBase):
    """Schema for creating a ticket."""
    pass


class TicketUpdate(BaseModel):
    """Schema for updating a ticket."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TicketStatus] = Field(None)
    priority: Optional[TicketPriority] = Field(None)
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketAssign(BaseModel):
    """Schema for assigning a ticket to a user."""
    assignee_id: UUID

    class Config:
        from_attributes = True


class TicketResponse(TicketBase):
    """Schema for ticket responses."""
    id: UUID
    project_id: UUID
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True
