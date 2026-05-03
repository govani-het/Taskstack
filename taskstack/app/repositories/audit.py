"""Audit helpers for repository write operations."""

from datetime import datetime, timezone
from uuid import UUID


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def mark_updated(model, updated_by: UUID | None = None) -> None:
    """Apply update audit fields to an ORM model when present."""
    if hasattr(model, "updated_at"):
        model.updated_at = utc_now()
    if updated_by is not None and hasattr(model, "updated_by"):
        model.updated_by = updated_by


def mark_deleted(model, deleted_by: UUID | None = None) -> None:
    """Apply soft-delete and delete audit fields to an ORM model."""
    deleted_at = utc_now()
    if hasattr(model, "is_active"):
        model.is_active = False
    if hasattr(model, "updated_at"):
        model.updated_at = deleted_at
    if hasattr(model, "deleted_at"):
        model.deleted_at = deleted_at
    if deleted_by is not None and hasattr(model, "deleted_by"):
        model.deleted_by = deleted_by


def mark_reactivated(model, updated_by: UUID | None = None) -> None:
    """Reactivate a soft-deleted model and clear delete audit fields."""
    if hasattr(model, "is_active"):
        model.is_active = True
    if hasattr(model, "deleted_at"):
        model.deleted_at = None
    if hasattr(model, "deleted_by"):
        model.deleted_by = None
    mark_updated(model, updated_by)
