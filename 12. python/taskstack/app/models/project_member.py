"""Project member ORM model."""

from app.config.database import Base
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
import uuid

class ProjectMember(Base):
    """Represents a project member record."""
    __tablename__ = "project_members"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)

    joined_at = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    project_manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    project_manager = relationship("User",foreign_keys=[project_manager_id])

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
        UniqueConstraint("project_id", "id", name="uq_project_member_project_and_id"),
    )

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships", foreign_keys=[user_id])
    role = relationship("Role", back_populates="project_members")

    created_tickets = relationship("Ticket", back_populates="created_by_member", foreign_keys="Ticket.created_by")
    assigned_tickets = relationship("Ticket", back_populates="assignee_member", foreign_keys="Ticket.assignee_id")
    updated_tickets = relationship("Ticket", back_populates="updated_by_member", foreign_keys="Ticket.updated_by")
    deleted_tickets = relationship("Ticket", back_populates="deleted_by_member", foreign_keys="Ticket.deleted_by")
    resolved_tickets = relationship("Ticket", back_populates="resolved_by_member", foreign_keys="Ticket.resolved_by")
    created_comments = relationship("Comment", back_populates="created_by_member", foreign_keys="Comment.created_by")
    updated_comments = relationship("Comment", back_populates="updated_by_member", foreign_keys="Comment.updated_by")
    deleted_comments = relationship("Comment", back_populates="deleted_by_member", foreign_keys="Comment.deleted_by")
    created_replies = relationship("Reply", back_populates="created_by_member", foreign_keys="Reply.created_by")
    updated_replies = relationship("Reply", back_populates="updated_by_member", foreign_keys="Reply.updated_by")
    deleted_replies = relationship("Reply", back_populates="deleted_by_member", foreign_keys="Reply.deleted_by")
    created_work_logs = relationship("WorkLog", back_populates="created_by_member", foreign_keys="WorkLog.created_by")
    updated_work_logs = relationship("WorkLog", back_populates="updated_by_member", foreign_keys="WorkLog.updated_by")
    deleted_work_logs = relationship("WorkLog", back_populates="deleted_by_member", foreign_keys="WorkLog.deleted_by")
