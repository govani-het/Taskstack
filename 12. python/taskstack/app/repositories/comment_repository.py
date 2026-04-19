"""Comment repository functions."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.comment import Comment


async def get_comments_by_ticket(db: AsyncSession, ticket_id: UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
    stmt = (
        select(Comment)
        .where(Comment.ticket_id == ticket_id, Comment.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_comment_by_id(db: AsyncSession, comment_id: UUID) -> Comment:
    stmt = select(Comment).where(Comment.id == comment_id, Comment.is_active == True)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_comment(db: AsyncSession, comment_data: dict) -> Comment:
    comment = Comment(**comment_data)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(db: AsyncSession, comment_id: UUID, update_data: dict) -> Comment:
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
    stmt = select(Comment).where(Comment.id == comment_id, Comment.is_active == True)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment:
        comment.is_active = False
        comment.deleted_by = deleted_by
        await db.commit()
        await db.refresh(comment)
    return comment
