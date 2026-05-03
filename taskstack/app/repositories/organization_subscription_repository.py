"""OrganizationSubscription repository functions."""

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.organization_subscription import OrganizationSubscription
from app.repositories.audit import utc_now


async def get_organization_subscription_by_id(db: AsyncSession, subscription_id: UUID) -> Optional[OrganizationSubscription]:
    """Get organization subscription by ID.

    Args:
        db: Database session.
        subscription_id: Organization subscription identifier.

    Returns:
        Optional[OrganizationSubscription]: Result of the operation.
    """
    stmt = select(OrganizationSubscription).where(
        OrganizationSubscription.id == subscription_id,
        OrganizationSubscription.is_active == True,
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_active_subscriptions_by_organization(db: AsyncSession, organization_id: UUID) -> List[OrganizationSubscription]:
    """Get active subscriptions for an organization.

    Args:
        db: Database session.
        organization_id: Organization identifier.

    Returns:
        List[OrganizationSubscription]: Result of the operation.
    """
    stmt = (
        select(OrganizationSubscription)
        .where(
            and_(
                OrganizationSubscription.organization_id == organization_id,
                OrganizationSubscription.is_active == True,
                OrganizationSubscription.cancelled_at.is_(None)
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_subscription_by_org_and_plan(db: AsyncSession, organization_id: UUID, subscription_id: UUID) -> Optional[OrganizationSubscription]:
    """Get active subscription for organization and plan.

    Args:
        db: Database session.
        organization_id: Organization identifier.
        subscription_id: Subscription plan identifier.

    Returns:
        Optional[OrganizationSubscription]: Result of the operation.
    """
    stmt = (
        select(OrganizationSubscription)
        .where(
            and_(
                OrganizationSubscription.organization_id == organization_id,
                OrganizationSubscription.subscription_id == subscription_id,
                OrganizationSubscription.is_active == True,
                OrganizationSubscription.cancelled_at.is_(None)
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_organization_subscription(db: AsyncSession, subscription_data: dict) -> OrganizationSubscription:
    """Create an organization subscription.

    Args:
        db: Database session.
        subscription_data: Subscription creation payload.

    Returns:
        OrganizationSubscription: The created resource.
    """
    subscription = OrganizationSubscription(**subscription_data)
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def cancel_organization_subscription(db: AsyncSession, subscription_id: UUID, cancelled_by: UUID) -> Optional[OrganizationSubscription]:
    """Cancel an organization subscription.

    Args:
        db: Database session.
        subscription_id: Organization subscription identifier.
        cancelled_by: User who cancelled the subscription.

    Returns:
        Optional[OrganizationSubscription]: Result of the operation.
    """
    cancelled_at = utc_now()
    stmt = (
        update(OrganizationSubscription)
        .where(OrganizationSubscription.id == subscription_id, OrganizationSubscription.is_active == True)
        .values(
            cancelled_at=cancelled_at,
            cancelled_by=cancelled_by,
            is_active=False,
            updated_at=cancelled_at,
            updated_by=cancelled_by,
            deleted_at=cancelled_at,
            deleted_by=cancelled_by,
        )
        .returning(OrganizationSubscription)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def get_organization_subscriptions(db: AsyncSession, organization_id: UUID, skip: int = 0, limit: int = 100) -> List[OrganizationSubscription]:
    """Get all subscriptions for an organization.

    Args:
        db: Database session.
        organization_id: Organization identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[OrganizationSubscription]: Result of the operation.
    """
    stmt = (
        select(OrganizationSubscription)
        .where(
            OrganizationSubscription.organization_id == organization_id,
            OrganizationSubscription.is_active == True,
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
