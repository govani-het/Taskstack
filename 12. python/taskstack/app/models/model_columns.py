"""Reusable ORM column mixins."""

from sqlalchemy import Column, DateTime, ForeignKey, UUID, func
from sqlalchemy.orm import declared_attr


class TimestampRequiredMixin:
    """Adds required timestamp fields to ORM models."""
    @declared_attr
    def created_at(cls):
        """Define the created_at column."""
        return Column(
            DateTime(timezone=True),
            nullable=False,
            default=func.now(),
            server_default=func.now(),
        )

    @declared_attr
    def updated_at(cls):
        """Define the updated_at column."""
        return Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        """Define the deleted_at column."""
        return Column(DateTime(timezone=True), nullable=True)


class TimestampOptionalMixin:
    """Adds optional timestamp fields to ORM models."""
    @declared_attr
    def created_at(cls):
        """Define the created_at column."""
        return Column(
            DateTime(timezone=True),
            nullable=True,
            default=func.now(),
            server_default=func.now(),
        )

    @declared_attr
    def updated_at(cls):
        """Define the updated_at column."""
        return Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        """Define the deleted_at column."""
        return Column(DateTime(timezone=True), nullable=True)


class UserAuditMixin:
    """Adds user audit foreign keys to ORM models."""
    @declared_attr
    def created_by(cls):
        """Define the created_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    @declared_attr
    def updated_by(cls):
        """Define the updated_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        """Define the deleted_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class ProjectMemberAuditMixin:
    """Adds project member audit foreign keys to ORM models."""
    @declared_attr
    def created_by(cls):
        """Define the created_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=False)

    @declared_attr
    def updated_by(cls):
        """Define the updated_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        """Define the deleted_by column."""
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=True)
