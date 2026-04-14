from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.roles import Role


async def get_role_by_id(db: AsyncSession, role_id: UUID) -> Optional[Role]:
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_role_by_name(db: AsyncSession, name: str) -> Optional[Role]:
    stmt = select(Role).where(Role.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
    stmt = select(Role).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_role(db: AsyncSession, role_data: dict) -> Role:
    role = Role(**role_data)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def update_role(db: AsyncSession, role_id: UUID, update_data: dict) -> Optional[Role]:
    stmt = (
        update(Role)
        .where(Role.id == role_id)
        .values(**update_data)
        .returning(Role)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_role(db: AsyncSession, role_id: UUID) -> bool:
    stmt = delete(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0