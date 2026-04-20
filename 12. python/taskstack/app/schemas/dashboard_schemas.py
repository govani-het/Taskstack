"""Dashboard schema definitions."""

from typing import Optional
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    """Schema for dashboard summary response."""
    total_projects: int
    active_projects: int
    total_tickets: int
    pending_tickets: int
    in_progress_tickets: int
    completed_tickets: int
    canceled_tickets: int
    total_members: int
    active_members: int

    class Config:
        from_attributes = True