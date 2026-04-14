from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.repositories.subscription_repository import (
    get_subscription_by_id,
    get_subscription_by_name,
    get_subscriptions,
    create_subscription,
    update_subscription,
    delete_subscription,
)
from app.schemas.subscription_schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse


async def create_subscription_service(db: AsyncSession, subscription_data: SubscriptionCreate) -> SubscriptionResponse:
    # Check if plan name already exists
    existing_subscription = await get_subscription_by_name(db, subscription_data.plan_name)
    if existing_subscription:
        raise ValueError("Subscription plan name already exists")

    subscription_dict = subscription_data.model_dump()
    subscription = await create_subscription(db, subscription_dict)
    return SubscriptionResponse.model_validate(subscription)


async def get_subscription_service(db: AsyncSession, subscription_id: UUID) -> Optional[SubscriptionResponse]:
    subscription = await get_subscription_by_id(db, subscription_id)
    if subscription:
        return SubscriptionResponse.model_validate(subscription)
    return None


async def get_subscriptions_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[SubscriptionResponse]:
    subscriptions = await get_subscriptions(db, skip, limit)
    return [SubscriptionResponse.model_validate(subscription) for subscription in subscriptions]


async def update_subscription_service(db: AsyncSession, subscription_id: UUID, update_data: SubscriptionUpdate) -> Optional[SubscriptionResponse]:
    update_dict = update_data.model_dump(exclude_unset=True)

    # Check name uniqueness if changing name
    if "plan_name" in update_dict:
        existing_subscription = await get_subscription_by_name(db, update_dict["plan_name"])
        if existing_subscription and existing_subscription.id != subscription_id:
            raise ValueError("Subscription plan name already exists")

    subscription = await update_subscription(db, subscription_id, update_dict)
    if subscription:
        return SubscriptionResponse.model_validate(subscription)
    return None


async def delete_subscription_service(db: AsyncSession, subscription_id: UUID) -> bool:
    return await delete_subscription(db, subscription_id)