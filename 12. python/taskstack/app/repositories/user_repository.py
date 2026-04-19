"""User repository functions."""

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.users import User


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """Fetch a user by ID.

    Args:
        db: Database session.
        user_id: User identifier.

    Returns:
        Optional[User]: Matching user, if found.
    """
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Fetch a user by email address.

    Args:
        db: Database session.
        email: Email address.

    Returns:
        Optional[User]: Matching user, if found.
    """
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .where(User.email == email)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Fetch users with pagination.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[User]: User records.
    """
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.organization))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: dict) -> User:
    """Create a user.

    Args:
        db: Database session.
        user_data: User creation payload.

    Returns:
        User: Newly created user.
    """
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: UUID, update_data: dict) -> Optional[User]:
    """Update a user.

    Args:
        db: Database session.
        user_id: User identifier.
        update_data: User update payload.

    Returns:
        Optional[User]: Updated user, if found.
    """
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_user(db: AsyncSession, user_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
    """Soft-delete a user.

    Args:
        db: Database session.
        user_id: User identifier.
        deleted_by: Identifier of the user deleting the record.

    Returns:
        bool: Whether the operation succeeded.
    """
    update_data = {"is_active": False}
    if deleted_by:
        update_data["deleted_by"] = deleted_by
    stmt = update(User).where(User.id == user_id).values(**update_data)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
