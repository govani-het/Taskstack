"""Subscription service layer."""

from fastapi import HTTPException, status
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


from app.schemas.response_schemas import APIResponse
from app.constant.subscription_constant import (
    SUCCESS_SUBSCRIPTION_CREATED,
    SUCCESS_SUBSCRIPTION_FETCHED,
    SUCCESS_SUBSCRIPTIONS_FETCHED,
    SUCCESS_SUBSCRIPTION_UPDATED,
    SUCCESS_SUBSCRIPTION_DELETED,
    ERROR_SUBSCRIPTION_PLAN_NAME_ALREADY_EXISTS,
    ERROR_SUBSCRIPTION_NOT_FOUND,
    ERROR_FAILED_TO_DELETE_SUBSCRIPTION,
    ROLE_SYSTEM_ADMIN,
)

class SubscriptionService:
    """Provides subscription business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def create_subscription_service(self, subscription_data: SubscriptionCreate) -> APIResponse[SubscriptionResponse]:
        """Create a subscription.

        Args:
            subscription_data: Subscription creation payload.

        Returns:
            APIResponse[SubscriptionResponse]: Standardized subscription creation response.
        """
        # Check if plan name already exists
        existing_subscription = await get_subscription_by_name(self.db, subscription_data.plan_name)
        if existing_subscription:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_SUBSCRIPTION_PLAN_NAME_ALREADY_EXISTS)

        subscription_dict = subscription_data.model_dump()
        try:
            subscription = await create_subscription(self.db, subscription_dict)
            return APIResponse.success_response(SUCCESS_SUBSCRIPTION_CREATED, SubscriptionResponse.model_validate(subscription))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_subscription_service(self, subscription_id: UUID) -> APIResponse[Optional[SubscriptionResponse]]:
        """Get a subscription by ID.

        Args:
            subscription_id: Subscription identifier.

        Returns:
            APIResponse[Optional[SubscriptionResponse]]: Standardized subscription lookup response.
        """
        subscription = await get_subscription_by_id(self.db, subscription_id)
        if subscription:
            return APIResponse.success_response(SUCCESS_SUBSCRIPTION_FETCHED, SubscriptionResponse.model_validate(subscription))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_SUBSCRIPTION_NOT_FOUND)

    async def get_subscriptions_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[SubscriptionResponse]]:
        """Get subscriptions with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[SubscriptionResponse]]: Standardized subscription list response.
        """
        subscriptions = await get_subscriptions(self.db, skip, limit)
        return APIResponse.success_response(SUCCESS_SUBSCRIPTIONS_FETCHED, [SubscriptionResponse.model_validate(subscription) for subscription in subscriptions])

    async def update_subscription_service(self, subscription_id: UUID, update_data: SubscriptionUpdate, updated_by: Optional[UUID] = None) -> APIResponse[Optional[SubscriptionResponse]]:
        """Update a subscription.

        Args:
            subscription_id: Subscription identifier.
            update_data: Subscription update payload.
            updated_by: Identifier of the user updating the record.

        Returns:
            APIResponse[Optional[SubscriptionResponse]]: Standardized subscription update response.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        # Check name uniqueness if changing name
        if "plan_name" in update_dict:
            existing_subscription = await get_subscription_by_name(self.db, update_dict["plan_name"])
            if existing_subscription and existing_subscription.id != subscription_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_SUBSCRIPTION_PLAN_NAME_ALREADY_EXISTS)

        if updated_by:
            update_dict["updated_by"] = updated_by

        subscription = await update_subscription(self.db, subscription_id, update_dict)
        if subscription:
            return APIResponse.success_response(SUCCESS_SUBSCRIPTION_UPDATED, SubscriptionResponse.model_validate(subscription))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_SUBSCRIPTION_NOT_FOUND)

    async def delete_subscription_service(self, subscription_id: UUID, deleted_by: Optional[UUID] = None) -> APIResponse[str]:
        """Soft-delete a subscription.

        Args:
            subscription_id: Subscription identifier.
            deleted_by: Identifier of the user deleting the record.

        Returns:
            APIResponse[str]: Standardized subscription deletion response.
        """
        response = await delete_subscription(self.db, subscription_id, deleted_by)
        if response:
            return APIResponse.success_response(SUCCESS_SUBSCRIPTION_DELETED)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_FAILED_TO_DELETE_SUBSCRIPTION)
