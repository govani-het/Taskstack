import uuid

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, String, UUID, UniqueConstraint
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.model_columns import ModelColumns


class Reply(Base):
    __tablename__ = "replies"
    __table_args__ = (
        UniqueConstraint("project_id", "id", name="uq_replies_project_and_id"),
        ForeignKeyConstraint(
            ["project_id", "comment_id"],
            ["comments.project_id", "comments.id"],
            name="fk_replies_comment_project_match",
        ),
        ForeignKeyConstraint(
            ["project_id", "created_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_replies_created_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "updated_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_replies_updated_by_project_member",
        ),
        ForeignKeyConstraint(
            ["project_id", "deleted_by"],
            ["project_members.project_id", "project_members.id"],
            name="fk_replies_deleted_by_project_member",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=False)
    reply = Column(String(1000), nullable=False)

    created_at = ModelColumns.created_at(nullable=False)
    updated_at = ModelColumns.updated_at(nullable=True)
    deleted_at = ModelColumns.deleted_at(nullable=True)

    created_by = ModelColumns.created_by_project_member(nullable=False)
    updated_by = ModelColumns.updated_by_project_member(nullable=True)
    deleted_by = ModelColumns.deleted_by_project_member(nullable=True)

    comment = relationship("Comment", back_populates="replies", foreign_keys=[comment_id])
    created_by_member = relationship(
        "ProjectMember", foreign_keys=[created_by], back_populates="created_replies"
    )
    updated_by_member = relationship(
        "ProjectMember", foreign_keys=[updated_by], back_populates="updated_replies"
    )
    deleted_by_member = relationship(
        "ProjectMember", foreign_keys=[deleted_by], back_populates="deleted_replies"
    )
