from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.organization import Organization


async def get_organization_by_id(db: AsyncSession, organization_id: UUID) -> Optional[Organization]:
    stmt = (
        select(Organization)
        .options(selectinload(Organization.subscription_plan), selectinload(Organization.users))
        .where(Organization.id == organization_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organization_by_name(db: AsyncSession, name: str) -> Optional[Organization]:
    stmt = select(Organization).where(Organization.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organization_by_email(db: AsyncSession, email: str) -> Optional[Organization]:
    stmt = select(Organization).where(Organization.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Organization]:
    stmt = (
        select(Organization)
        .options(selectinload(Organization.subscription_plan), selectinload(Organization.users))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_unapproved_organizations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Organization]:
    stmt = (
        select(Organization)
        .options(selectinload(Organization.subscription_plan), selectinload(Organization.users))
        .where(Organization.is_approved == False)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_organization(db: AsyncSession, organization_data: dict) -> Organization:
    organization = Organization(**organization_data)
    db.add(organization)
    await db.commit()
    await db.refresh(organization)
    return organization


async def update_organization(db: AsyncSession, organization_id: UUID, update_data: dict) -> Optional[Organization]:
    stmt = (
        update(Organization)
        .where(Organization.id == organization_id)
        .values(**update_data)
        .returning(Organization)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_organization(db: AsyncSession, organization_id: UUID) -> bool:
    stmt = delete(Organization).where(Organization.id == organization_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0