from sqlalchemy import Column, DateTime, ForeignKey, UUID, func
from sqlalchemy.orm import declared_attr


class TimestampRequiredMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime(timezone=True), nullable=True)


class TimestampOptionalMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), nullable=True, server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime(timezone=True), nullable=True)


class UserAuditMixin:
    @declared_attr
    def created_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    @declared_attr
    def updated_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class ProjectMemberAuditMixin:
    @declared_attr
    def created_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=False)

    @declared_attr
    def updated_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)
