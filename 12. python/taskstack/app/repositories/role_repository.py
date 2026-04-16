"""Role repository functions."""

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.roles import Role


async def get_role_by_id(db: AsyncSession, role_id: UUID) -> Optional[Role]:
    """Get role.
    
    Args:
        db: Database session.
        role_id: Role identifier.
    
    Returns:
        Optional[Role]: Result of the operation.
    """
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_role_by_name(db: AsyncSession, name: str) -> Optional[Role]:
    """Get role.
    
    Args:
        db: Database session.
        name: Name value.
    
    Returns:
        Optional[Role]: Result of the operation.
    """
    stmt = select(Role).where(Role.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
    """Get roles.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Role]: Result of the operation.
    """
    stmt = select(Role).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_role(db: AsyncSession, role_data: dict) -> Role:
    """Create a role.
    
    Args:
        db: Database session.
        role_data: Payload for creating a role.
    
    Returns:
        Role: The created resource.
    """
    role = Role(**role_data)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def update_role(db: AsyncSession, role_id: UUID, update_data: dict) -> Optional[Role]:
    """Update a role.
    
    Args:
        db: Database session.
        role_id: Role identifier.
        update_data: Role update payload.
    
    Returns:
        Optional[Role]: Result of the operation.
    """
    stmt = (
        update(Role)
        .where(Role.id == role_id)
        .values(**update_data)
        .returning(Role)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_role(db: AsyncSession, role_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
    """Delete a role.
    
    Args:
        db: Database session.
        role_id: Role identifier.
        deleted_by: Identifier of the user deleting the record.
    
    Returns:
        bool: Whether the operation succeeded.
    """
    update_data = {"is_active": False}
    if deleted_by:
        update_data["deleted_by"] = deleted_by
    stmt = update(Role).where(Role.id == role_id).values(**update_data)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
