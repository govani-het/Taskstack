"""Subscription repository functions."""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.subscription import Subscription


async def get_subscription_by_id(db: AsyncSession, subscription_id: UUID) -> Optional[Subscription]:
    """Get subscription.
    
    Args:
        db: Database session.
        subscription_id: Subscription identifier.
    
    Returns:
        Optional[Subscription]: Result of the operation.
    """
    stmt = select(Subscription).where(Subscription.id == subscription_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_subscription_by_name(db: AsyncSession, plan_name: str) -> Optional[Subscription]:
    """Get subscription.
    
    Args:
        db: Database session.
        plan_name: Subscription plan name.
    
    Returns:
        Optional[Subscription]: Result of the operation.
    """
    stmt = select(Subscription).where(Subscription.plan_name == plan_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_subscriptions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Subscription]:
    """Get subscriptions.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Subscription]: Result of the operation.
    """
    stmt = select(Subscription).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_subscription(db: AsyncSession, subscription_data: dict) -> Subscription:
    """Create a subscription.
    
    Args:
        db: Database session.
        subscription_data: Payload for creating a subscription.
    
    Returns:
        Subscription: The created resource.
    """
    subscription = Subscription(**subscription_data)
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def update_subscription(db: AsyncSession, subscription_id: UUID, update_data: dict) -> Optional[Subscription]:
    """Update a subscription.
    
    Args:
        db: Database session.
        subscription_id: Subscription identifier.
        update_data: Subscription update payload.
    
    Returns:
        Optional[Subscription]: Result of the operation.
    """
    stmt = (
        update(Subscription)
        .where(Subscription.id == subscription_id)
        .values(**update_data)
        .returning(Subscription)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_subscription(db: AsyncSession, subscription_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
    """Delete a subscription.
    
    Args:
        db: Database session.
        subscription_id: Subscription identifier.
        deleted_by: Identifier of the user deleting the record.
    
    Returns:
        bool: Whether the operation succeeded.
    """
    update_data = {"is_active": False}
    if deleted_by:
        update_data["deleted_by"] = deleted_by
    stmt = update(Subscription).where(Subscription.id == subscription_id).values(**update_data)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
