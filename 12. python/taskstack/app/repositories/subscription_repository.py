from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.subscription import Subscription


async def get_subscription_by_id(db: AsyncSession, subscription_id: UUID) -> Optional[Subscription]:
    stmt = select(Subscription).where(Subscription.id == subscription_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_subscription_by_name(db: AsyncSession, plan_name: str) -> Optional[Subscription]:
    stmt = select(Subscription).where(Subscription.plan_name == plan_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_subscriptions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Subscription]:
    stmt = select(Subscription).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_subscription(db: AsyncSession, subscription_data: dict) -> Subscription:
    subscription = Subscription(**subscription_data)
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def update_subscription(db: AsyncSession, subscription_id: UUID, update_data: dict) -> Optional[Subscription]:
    stmt = (
        update(Subscription)
        .where(Subscription.id == subscription_id)
        .values(**update_data)
        .returning(Subscription)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_subscription(db: AsyncSession, subscription_id: UUID) -> bool:
    stmt = delete(Subscription).where(Subscription.id == subscription_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0