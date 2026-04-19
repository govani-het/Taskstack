"""Reply repository functions."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.reply import Reply


async def get_replies_by_comment(db: AsyncSession, comment_id: UUID, skip: int = 0, limit: int = 100) -> List[Reply]:
    stmt = (
        select(Reply)
        .where(Reply.comment_id == comment_id, Reply.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_reply_by_id(db: AsyncSession, reply_id: UUID) -> Reply:
    stmt = select(Reply).where(Reply.id == reply_id, Reply.is_active == True)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_reply(db: AsyncSession, reply_data: dict) -> Reply:
    reply = Reply(**reply_data)
    db.add(reply)
    await db.commit()
    await db.refresh(reply)
    return reply


async def update_reply(db: AsyncSession, reply_id: UUID, update_data: dict) -> Reply:
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
    stmt = select(Reply).where(Reply.id == reply_id, Reply.is_active == True)
    result = await db.execute(stmt)
    reply = result.scalar_one_or_none()
    if reply:
        reply.is_active = False
        reply.deleted_by = deleted_by
        await db.commit()
        await db.refresh(reply)
    return reply