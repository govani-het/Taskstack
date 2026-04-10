import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    UUID,
    func,
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class WorkLog(Base):
    __tablename__ = "work_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "ticket_id"],
            ["tickets.project_id", "tickets.id"],
            name="fk_work_logs_ticket_project_match",
        ),
        ForeignKeyConstraint(
            ["project_id", "created_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_work_logs_created_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "updated_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_work_logs_updated_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "deleted_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_work_logs_deleted_by_project_member",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)
    description = Column(String(1000), nullable=True)
    time_spent_minutes = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    created_by = Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)

    ticket = relationship("Ticket", back_populates="work_logs", foreign_keys=[ticket_id])
    created_by_member = relationship(
        "ProjectMember", foreign_keys=[created_by], back_populates="created_work_logs"
    )
    updated_by_member = relationship(
        "ProjectMember", foreign_keys=[updated_by], back_populates="updated_work_logs"
    )
    deleted_by_member = relationship(
        "ProjectMember", foreign_keys=[deleted_by], back_populates="deleted_work_logs"
    )
