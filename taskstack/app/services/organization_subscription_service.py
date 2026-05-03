"""OrganizationSubscription service layer."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.organization_subscription import OrganizationSubscription
from app.repositories.organization_subscription_repository import (
    get_organization_subscription_by_id,
    get_active_subscriptions_by_organization,
    get_subscription_by_org_and_plan,
    create_organization_subscription,
    cancel_organization_subscription,
    get_organization_subscriptions,
)
from app.repositories.organization_repository import get_organization_by_id
from app.repositories.subscription_repository import get_subscription_by_id
from app.repositories.project_repository import get_projects_by_organization
from app.schemas.organization_subscription_schemas import (
    OrganizationSubscriptionCreate,
    OrganizationSubscriptionResponse,
    OrganizationSubscriptionBasicResponse,
)
from app.schemas.response_schemas import APIResponse
from app.constant.role_constant import ROLE_ADMIN


class OrganizationSubscriptionService:
    """Provides organization subscription business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def buy_subscription_service(
        self,
        organization_id: UUID,
        subscription_data: OrganizationSubscriptionCreate,
        current_user: dict
    ) -> APIResponse[OrganizationSubscriptionResponse]:
        """Buy a subscription for an organization.

        Args:
            organization_id: Organization identifier.
            subscription_data: Subscription creation payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[OrganizationSubscriptionResponse]: Standardized response.

        Raises:
            HTTPException: If validation fails.
        """
        # Validate user is admin of the organization
        if current_user.get("role") != ROLE_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can buy subscriptions"
            )

        if str(current_user.get("organization_id")) != str(organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins can only manage their own organization's subscriptions"
            )

        # Check if organization exists
        organization = await get_organization_by_id(self.db, organization_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )

        # Check if subscription plan exists
        subscription = await get_subscription_by_id(self.db, subscription_data.subscription_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription plan not found"
            )

        # Check if organization already has this active subscription
        existing_subscription = await get_subscription_by_org_and_plan(
            self.db, organization_id, subscription_data.subscription_id
        )
        if existing_subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization already has an active subscription for this plan"
            )

        # Create the subscription
        subscription_dict = {
            "organization_id": organization_id,
            "subscription_id": subscription_data.subscription_id,
            "created_by": UUID(current_user["id"]),
        }

        try:
            org_subscription = await create_organization_subscription(self.db, subscription_dict)
            return APIResponse.success_response(
                "Subscription purchased successfully",
                OrganizationSubscriptionResponse.model_validate(org_subscription)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create subscription: {str(e)}"
            )

    async def cancel_subscription_service(
        self,
        organization_id: UUID,
        subscription_id: UUID,
        current_user: dict
    ) -> APIResponse[str]:
        """Cancel a subscription for an organization.

        Args:
            organization_id: Organization identifier.
            subscription_id: Organization subscription identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[str]: Standardized response.

        Raises:
            HTTPException: If validation fails.
        """
        # Validate user is admin of the organization
        if current_user.get("role") != ROLE_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can cancel subscriptions"
            )

        if str(current_user.get("organization_id")) != str(organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins can only manage their own organization's subscriptions"
            )

        # Check if organization subscription exists and is active
        org_subscription = await get_organization_subscription_by_id(self.db, subscription_id)
        if not org_subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        if str(org_subscription.organization_id) != str(organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Subscription does not belong to this organization"
            )

        if not org_subscription.is_active or org_subscription.cancelled_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subscription is already cancelled"
            )

        # Cancel the subscription
        try:
            await cancel_organization_subscription(self.db, subscription_id, UUID(current_user["id"]))
            return APIResponse.success_response("Subscription cancelled successfully")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel subscription: {str(e)}"
            )

    async def get_organization_subscriptions_service(
        self,
        organization_id: UUID,
        current_user: dict,
        skip: int = 0,
        limit: int = 100
    ) -> APIResponse[List[OrganizationSubscriptionBasicResponse]]:
        """Get subscriptions for an organization.

        Args:
            organization_id: Organization identifier.
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[OrganizationSubscriptionBasicResponse]]: Standardized response.

        Raises:
            HTTPException: If validation fails.
        """
        # Validate user has access to organization
        if current_user.get("role") != ROLE_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can view organization subscriptions"
            )

        if str(current_user.get("organization_id")) != str(organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins can only view their own organization's subscriptions"
            )

        try:
            subscriptions = await get_organization_subscriptions(self.db, organization_id, skip, limit)
            return APIResponse.success_response(
                "Subscriptions retrieved successfully",
                [OrganizationSubscriptionBasicResponse.model_validate(sub) for sub in subscriptions]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve subscriptions: {str(e)}"
            )

    async def get_active_subscriptions_service(self, organization_id: UUID) -> List[OrganizationSubscription]:
        """Get active subscriptions for an organization (internal use).

        Args:
            organization_id: Organization identifier.

        Returns:
            List[OrganizationSubscription]: Active subscriptions.
        """
        return await get_active_subscriptions_by_organization(self.db, organization_id)

    async def check_project_creation_limit(self, organization_id: UUID) -> bool:
        """Check if organization can create more projects based on active subscriptions.

        Args:
            organization_id: Organization identifier.

        Returns:
            bool: Whether project creation is allowed.
        """
        active_subscriptions = await self.get_active_subscriptions_service(organization_id)

        # Count active projects
        projects = await get_projects_by_organization(self.db, organization_id)
        active_project_count = sum(1 for project in projects if project.is_active)

        # Calculate total allowed projects based on active subscriptions from database
        total_allowed = 0
        for sub in active_subscriptions:
            total_allowed += sub.subscription.allowed_projects

        return active_project_count < total_allowed

    async def check_subscription_access(self, organization_id: UUID) -> bool:
        """Check if organization has any active subscriptions.

        Args:
            organization_id: Organization identifier.

        Returns:
            bool: Whether organization has active subscriptions.
        """
        active_subscriptions = await self.get_active_subscriptions_service(organization_id)
        return len(active_subscriptions) > 0