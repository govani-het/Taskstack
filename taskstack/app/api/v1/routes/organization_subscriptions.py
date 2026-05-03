"""OrganizationSubscription API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.organization_subscription_schemas import (
    OrganizationSubscriptionCreate,
    OrganizationSubscriptionBasicResponse,
)
from app.services.organization_subscription_service import OrganizationSubscriptionService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

from app.constant.role_constant import ROLE_ADMIN

router = APIRouter(
    prefix="/organizations/{organization_id}/subscriptions",
    tags=["organization-subscriptions"],
)


@router.post("/", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
@require_roles([ROLE_ADMIN])
async def buy_subscription(
    organization_id: UUID,
    subscription_data: OrganizationSubscriptionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Buy a subscription for an organization.

    Args:
        organization_id: Organization identifier.
        subscription_data: Subscription creation payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = OrganizationSubscriptionService(db)
    return await subscription_obj.buy_subscription_service(organization_id, subscription_data, current_user)


@router.patch("/{subscription_id}/cancel", response_model=APIResponse[str])
@require_roles([ROLE_ADMIN])
async def cancel_subscription(
    organization_id: UUID,
    subscription_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Cancel a subscription for an organization.

    Args:
        organization_id: Organization identifier.
        subscription_id: Organization subscription identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = OrganizationSubscriptionService(db)
    return await subscription_obj.cancel_subscription_service(organization_id, subscription_id, current_user)


@router.get("/", response_model=APIResponse[List[OrganizationSubscriptionBasicResponse]])
@require_roles([ROLE_ADMIN])
async def get_organization_subscriptions(
    organization_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get subscriptions for an organization.

    Args:
        organization_id: Organization identifier.
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    subscription_obj = OrganizationSubscriptionService(db)
    return await subscription_obj.get_organization_subscriptions_service(organization_id, current_user, skip, limit)