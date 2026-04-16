"""Organization service layer."""

from http.client import responses

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.repositories.organization_repository import (
    get_organization_by_id,
    get_organization_by_email,
    get_organizations,
    get_unapproved_organizations,
    create_organization,
    update_organization,
    delete_organization,
)
from app.repositories.subscription_repository import get_subscription_by_id
from app.schemas.organization_schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.schemas.response_schemas import APIResponse

class OrganizationService:
    """Provides organization business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def validate_subscription_exists(self, subscription_id: UUID) -> bool:
        """Check whether a subscription exists.

        Args:
            subscription_id: Subscription identifier.

        Returns:
            bool: Whether the subscription exists.
        """
        subscription = await get_subscription_by_id(self.db, subscription_id)
        return subscription is not None


    async def create_organization_service(self, organization_data: OrganizationCreate, created_by: Optional[UUID] = None) -> APIResponse[OrganizationResponse]:
        """Create an organization.

        Args:
            organization_data: Organization creation payload.
            created_by: Identifier of the user creating the record.

        Returns:
            APIResponse[OrganizationResponse]: Standardized organization creation response.

        Raises:
            ValueError: If the email or subscription plan is invalid.
        """
        existing_organization = await get_organization_by_email(self.db, organization_data.email)
        if existing_organization:
            raise ValueError("Organization email already registered")

        if organization_data.subscription_plan_id and not await self.validate_subscription_exists(organization_data.subscription_plan_id):
            raise ValueError("Invalid subscription plan ID")

        organization_dict = organization_data.model_dump()
        if created_by:
            organization_dict["created_by"] = created_by
        try:
            organization = await create_organization(self.db, organization_dict)
            if not organization:
                return APIResponse.error_response("Failed to create organization")
            return APIResponse.success_response("Organization created successfully", OrganizationResponse.model_validate(organization))
        except Exception as e:
            return APIResponse.error_response(str(e))

    async def get_organization_service(self, organization_id: UUID) -> APIResponse[Optional[OrganizationResponse]]:
        """Get an organization by ID.

        Args:
            organization_id: Organization identifier.

        Returns:
            APIResponse[Optional[OrganizationResponse]]: Standardized organization lookup response.
        """

        organization = await get_organization_by_id(self.db, organization_id)
        if organization:
            return APIResponse.success_response("Organization Fetch Successfully.", OrganizationResponse.model_validate(organization))
        return APIResponse.error_response("Failed to fetch organization")

    async def get_organizations_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[OrganizationResponse]]:
        """Get organizations with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[OrganizationResponse]]: Standardized organization list response.
        """
        organizations = await get_organizations(self.db, skip, limit)
        if not organizations:
            return APIResponse.error_response("Failed to fetch organizations")
        return APIResponse.success_response("SuccessFully fetch all organizations", [OrganizationResponse.model_validate(organization) for organization in organizations])

    async def get_unapproved_organizations_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[OrganizationResponse]]:
        """Get unapproved organizations with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[OrganizationResponse]]: Standardized unapproved-organization list response.
        """
        organizations = await get_unapproved_organizations(self.db, skip, limit)
        if not organizations:
            return APIResponse.error_response("Failed to fetch unapproved organizations")

        return APIResponse.success_response("Successfully Fetch unapproved organization", [OrganizationResponse.model_validate(organization) for organization in organizations])


    async def update_organization_service(self, organization_id: UUID, update_data: OrganizationUpdate, updated_by: Optional[UUID] = None) -> APIResponse[Optional[OrganizationResponse]]:
        """Update an organization.

        Args:
            organization_id: Organization identifier.
            update_data: Organization update payload.
            updated_by: Identifier of the user updating the record.

        Returns:
            APIResponse[Optional[OrganizationResponse]]: Standardized organization update response.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        if "subscription_plan_id" in update_dict and update_dict["subscription_plan_id"] and not await self.validate_subscription_exists(update_dict["subscription_plan_id"]):
            return APIResponse.error_response("Invalid subscription plan ID")

        if "email" in update_dict:
            existing_organization = await get_organization_by_email(self.db, update_dict["email"])
            if existing_organization and existing_organization.id != organization_id:
                return APIResponse.error_response("Organization email already registered")

        if updated_by:
            update_dict["updated_by"] = updated_by

        organization = await update_organization(self.db, organization_id, update_dict)
        if organization:
            return APIResponse.success_response("Successfully Update Organization", OrganizationResponse.model_validate(organization))
        return APIResponse.error_response("Failed to Update Organization")


    async def approve_organization_service(self, organization_id: UUID, approved_by: UUID) -> APIResponse[Optional[OrganizationResponse]]:
        """Approve an organization.

        Args:
            organization_id: Organization identifier.
            approved_by: Identifier of the user approving the organization.

        Returns:
            APIResponse[Optional[OrganizationResponse]]: Standardized organization approval response.
        """
        response = await self.update_organization_service(organization_id, OrganizationUpdate(is_approved=True), approved_by)
        if response:
            return APIResponse.success_response("Successfully Approved Organization")
        return APIResponse.error_response("Failed to Approve Organization")

    async def delete_organization_service(self, organization_id: UUID, deleted_by: Optional[UUID] = None) -> APIResponse[str]:
        """Soft-delete an organization.

        Args:
            organization_id: Organization identifier.
            deleted_by: Identifier of the user deleting the record.

        Returns:
            APIResponse[str]: Standardized organization deletion response.
        """
        response = await delete_organization(self.db, organization_id, deleted_by)
        if not response:
            return APIResponse.error_response("Failed to Delete Organization")
        return APIResponse.success_response("Successfully Delete Organization")
