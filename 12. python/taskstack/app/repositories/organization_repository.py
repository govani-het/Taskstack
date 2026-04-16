"""Organization repository functions."""

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.organization import Organization
from app.utils.hash_password import hash_password

from app.models.users import User
from app.models.roles import Role


async def get_organization_by_id(db: AsyncSession, organization_id: UUID) -> Optional[Organization]:
    """Get organization.
    
    Args:
        db: Database session.
        organization_id: Organization identifier.
    
    Returns:
        Optional[Organization]: Result of the operation.
    """
    stmt = (
        select(Organization)
        .options(selectinload(Organization.subscription_plan), selectinload(Organization.users))
        .where(Organization.id == organization_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organization_by_name(db: AsyncSession, name: str) -> Optional[Organization]:
    """Get organization.
    
    Args:
        db: Database session.
        name: Name value.
    
    Returns:
        Optional[Organization]: Result of the operation.
    """
    stmt = select(Organization).where(Organization.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organization_by_email(db: AsyncSession, email: str) -> Optional[Organization]:
    """Get organization.
    
    Args:
        db: Database session.
        email: Email address.
    
    Returns:
        Optional[Organization]: Result of the operation.
    """
    stmt = select(Organization).where(Organization.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Organization]:
    """Get organizations.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Organization]: Result of the operation.
    """
    stmt = (
        select(Organization)
        .options(selectinload(Organization.subscription_plan), selectinload(Organization.users))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_unapproved_organizations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Organization]:
    """Get unapproved organizations.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Organization]: Result of the operation.
    """
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
    """Create an organization.
    
    Args:
        db: Database session.
        organization_data: Payload for creating an organization.
    
    Returns:
        Organization: The created resource.
    
    Raises:
        Exception: If the operation cannot be completed.
    """
    user_password = organization_data.pop("password")
    first_name = organization_data.pop("first_name")
    last_name = organization_data.pop("last_name")

    result = await db.execute(select(Role).where(Role.name == "admin"))
    admin_role = result.scalars().first()
    if not admin_role:
        raise Exception("Admin role not found in database")

    organization = Organization(**organization_data)
    db.add(organization)
    await db.flush()

    user_hash_password = hash_password(user_password)

    admin_user = User(
        first_name=first_name,
        last_name=last_name,
        email=organization.email,
        password=user_hash_password,
        role_id=admin_role.id,
        organization_id=organization.id,
    )
    db.add(admin_user)
    await db.commit()
    await db.refresh(organization)


    return organization


async def update_organization(db: AsyncSession, organization_id: UUID, update_data: dict) -> Optional[Organization]:
    """Update an organization.
    
    Args:
        db: Database session.
        organization_id: Organization identifier.
        update_data: Organization update payload.
    
    Returns:
        Optional[Organization]: Result of the operation.
    """
    stmt = (
        update(Organization)
        .where(Organization.id == organization_id)
        .values(**update_data)
        .returning(Organization)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_organization(db: AsyncSession, organization_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
    """Delete an organization.
    
    Args:
        db: Database session.
        organization_id: Organization identifier.
        deleted_by: Identifier of the user deleting the record.
    
    Returns:
        bool: Whether the operation succeeded.
    """
    update_data = {"is_active": False}
    if deleted_by:
        update_data["deleted_by"] = deleted_by
    stmt = update(Organization).where(Organization.id == organization_id).values(**update_data)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
