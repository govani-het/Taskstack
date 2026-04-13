from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.users import User


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.email == email)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: dict) -> User:
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: UUID, update_data: dict) -> Optional[User]:
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    stmt = delete(User).where(User.id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0