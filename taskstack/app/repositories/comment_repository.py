"""Comment repository functions."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.comment import Comment
from app.repositories.audit import mark_deleted


async def get_comments_by_ticket(db: AsyncSession, ticket_id: UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
    """Fetch active comments for a ticket.

    Args:
        db: Database session.
        ticket_id: Ticket identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Comment]: Active comments for the ticket.
    """
    stmt = (
        select(Comment)
        .where(Comment.ticket_id == ticket_id, Comment.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_comment_by_id(db: AsyncSession, comment_id: UUID) -> Comment:
    """Fetch an active comment by ID.

    Args:
        db: Database session.
        comment_id: Comment identifier.

    Returns:
        Comment: Matching active comment, if found.
    """
    stmt = select(Comment).where(Comment.id == comment_id, Comment.is_active == True)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_comment(db: AsyncSession, comment_data: dict) -> Comment:
    """Create a comment record.

    Args:
        db: Database session.
        comment_data: Comment field values.

    Returns:
        Comment: Newly created comment.
    """
    comment = Comment(**comment_data)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(db: AsyncSession, comment_id: UUID, update_data: dict) -> Comment:
    """Update an active comment.

    Args:
        db: Database session.
        comment_id: Comment identifier.
        update_data: Fields to update.

    Returns:
        Comment: Updated comment, if found.
    """
    stmt = select(Comment).where(Comment.id == comment_id, Comment.is_active == True)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment:
        for key, value in update_data.items():
            setattr(comment, key, value)
        await db.commit()
        await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: UUID, deleted_by: UUID) -> Comment:
    """Soft-delete an active comment.

    Args:
        db: Database session.
        comment_id: Comment identifier.
        deleted_by: Project member performing the deletion.

    Returns:
        Comment: Soft-deleted comment, if found.
    """
    stmt = select(Comment).where(Comment.id == comment_id, Comment.is_active == True)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment:
        mark_deleted(comment, deleted_by)
        await db.commit()
        await db.refresh(comment)
    return comment
