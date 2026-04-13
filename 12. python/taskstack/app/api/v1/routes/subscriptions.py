from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.schemas.subscription_schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services.subscription_service import (
    create_subscription_service,
    get_subscription_service,
    get_subscriptions_service,
    update_subscription_service,
    delete_subscription_service,
)
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import check_allowed_roles

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "create subscription plans")

    try:
        subscription = await create_subscription_service(db, subscription_data)
        return subscription
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    subscription = await get_subscription_service(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription


@router.get("/", response_model=List[SubscriptionResponse])
async def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await get_subscriptions_service(db, skip, limit)


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: UUID,
    update_data: SubscriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "update subscription plans")

    try:
        subscription = await update_subscription_service(db, subscription_id, update_data)
        if not subscription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return subscription
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "delete subscription plans")

    success = await delete_subscription_service(db, subscription_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")