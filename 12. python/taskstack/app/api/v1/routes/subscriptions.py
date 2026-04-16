"""Subscription API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.subscription_schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services.subscription_service import SubscriptionService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.post("/", response_model=APIResponse[SubscriptionResponse], status_code=status.HTTP_201_CREATED)
@require_roles(["system admin"])
async def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a subscription.

    Args:
        subscription_data: Subscription creation payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = SubscriptionService(db)
    return await subscription_obj.create_subscription_service(subscription_data)


@router.get("/{subscription_id}", response_model=APIResponse[SubscriptionResponse])
async def get_subscription(
    subscription_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a subscription by ID.

    Args:
        subscription_id: Subscription identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = SubscriptionService(db)
    return await subscription_obj.get_subscription_service(subscription_id)


@router.get("/", response_model=APIResponse[List[SubscriptionResponse]])
async def get_subscriptions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,

):
    """Get subscriptions with pagination.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    subscription_obj = SubscriptionService(db)
    return await subscription_obj.get_subscriptions_service(skip, limit)


@router.put("/{subscription_id}", response_model=APIResponse[SubscriptionResponse])
@require_roles(["system admin"])
async def update_subscription(
    subscription_id: UUID,
    update_data: SubscriptionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update a subscription.

    Args:
        subscription_id: Subscription identifier.
        update_data: Subscription update payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = SubscriptionService(db)
    return await subscription_obj.update_subscription_service(subscription_id, update_data, UUID(current_user["id"]))


@router.delete("/{subscription_id}", response_model=APIResponse[str], status_code=status.HTTP_200_OK)
@require_roles(["system admin"])
async def delete_subscription(
    subscription_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a subscription.

    Args:
        subscription_id: Subscription identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    subscription_obj = SubscriptionService(db)
    return await subscription_obj.delete_subscription_service(subscription_id, UUID(current_user["id"]))
