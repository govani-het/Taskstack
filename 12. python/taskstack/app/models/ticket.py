"""Ticket ORM model."""

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    UUID,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import ProjectMemberAuditMixin, TimestampRequiredMixin


class Ticket(TimestampRequiredMixin, ProjectMemberAuditMixin, Base):
    """Represents a ticket record."""
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("project_id", "id", name="uq_tickets_project_and_id"),
        ForeignKeyConstraint(
            ["project_id", "created_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_tickets_created_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "assignee_id"],
            ["project_members.project_id", "project_members.id"],
            name="fk_tickets_assignee_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "updated_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_tickets_updated_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "deleted_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_tickets_deleted_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "resolved_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_tickets_resolved_by_project_member",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    type = Column(String(50), nullable=False)  # e.g., Bug, Feature, Task
    status = Column(String(50), nullable=False, default="Open")  # e.g., Open, In Progress, Closed
    priority = Column(String(50), nullable=False, default="Medium")  # e.g., Low, Medium, High
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    ticket_type = Column(String(50), nullable=True)
    ticket_id = Column(Integer, nullable=True)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    project = relationship("Project", back_populates="tickets")
    created_by_member = relationship(
        "ProjectMember", foreign_keys="Ticket.created_by", back_populates="created_tickets"
    )
    assignee_member = relationship(
        "ProjectMember", foreign_keys=[assignee_id], back_populates="assigned_tickets"
    )
    updated_by_member = relationship(
        "ProjectMember", foreign_keys="Ticket.updated_by", back_populates="updated_tickets"
    )
    deleted_by_member = relationship(
        "ProjectMember", foreign_keys="Ticket.deleted_by", back_populates="deleted_tickets"
    )
    resolved_by_member = relationship(
        "ProjectMember", foreign_keys=[resolved_by], back_populates="resolved_tickets"
    )
    comments = relationship("Comment", back_populates="ticket", foreign_keys="Comment.ticket_id")
    work_logs = relationship("WorkLog", back_populates="ticket", foreign_keys="WorkLog.ticket_id")
