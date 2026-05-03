"""Reply repository functions."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.reply import Reply
from app.repositories.audit import mark_deleted


async def get_replies_by_comment(db: AsyncSession, comment_id: UUID, skip: int = 0, limit: int = 100) -> List[Reply]:
    """Fetch active replies for a comment.

    Args:
        db: Database session.
        comment_id: Comment identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Reply]: Active replies for the comment.
    """
    stmt = (
        select(Reply)
        .where(Reply.comment_id == comment_id, Reply.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_reply_by_id(db: AsyncSession, reply_id: UUID) -> Reply:
    """Fetch an active reply by ID.

    Args:
        db: Database session.
        reply_id: Reply identifier.

    Returns:
        Reply: Matching active reply, if found.
    """
    stmt = select(Reply).where(Reply.id == reply_id, Reply.is_active == True)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_reply(db: AsyncSession, reply_data: dict) -> Reply:
    """Create a reply record.

    Args:
        db: Database session.
        reply_data: Reply field values.

    Returns:
        Reply: Newly created reply.
    """
    reply = Reply(**reply_data)
    db.add(reply)
    await db.commit()
    await db.refresh(reply)
    return reply


async def update_reply(db: AsyncSession, reply_id: UUID, update_data: dict) -> Reply:
    """Update an active reply.

    Args:
        db: Database session.
        reply_id: Reply identifier.
        update_data: Fields to update.

    Returns:
        Reply: Updated reply, if found.
    """
    stmt = select(Reply).where(Reply.id == reply_id, Reply.is_active == True)
    result = await db.execute(stmt)
    reply = result.scalar_one_or_none()
    if reply:
        for key, value in update_data.items():
            setattr(reply, key, value)
        await db.commit()
        await db.refresh(reply)
    return reply


async def delete_reply(db: AsyncSession, reply_id: UUID, deleted_by: UUID) -> Reply:
    """Soft-delete an active reply.

    Args:
        db: Database session.
        reply_id: Reply identifier.
        deleted_by: Project member performing the deletion.

    Returns:
        Reply: Soft-deleted reply, if found.
    """
    stmt = select(Reply).where(Reply.id == reply_id, Reply.is_active == True)
    result = await db.execute(stmt)
    reply = result.scalar_one_or_none()
    if reply:
        mark_deleted(reply, deleted_by)
        await db.commit()
        await db.refresh(reply)
    return reply
