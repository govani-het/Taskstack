from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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


async def validate_subscription_exists(db: AsyncSession, subscription_id: UUID) -> bool:
    subscription = await get_subscription_by_id(db, subscription_id)
    return subscription is not None


async def create_organization_service(db: AsyncSession, organization_data: OrganizationCreate, created_by: Optional[UUID] = None) -> OrganizationResponse:
    # Check if email already exists
    existing_organization = await get_organization_by_email(db, organization_data.email)
    if existing_organization:
        raise ValueError("Organization email already registered")

    # Validate subscription if provided
    if organization_data.subscription_plan_id and not await validate_subscription_exists(db, organization_data.subscription_plan_id):
        raise ValueError("Invalid subscription plan ID")

    organization_dict = organization_data.model_dump()
    if created_by:
        organization_dict["created_by"] = created_by

    organization = await create_organization(db, organization_dict)
    return OrganizationResponse.model_validate(organization)


async def get_organization_service(db: AsyncSession, organization_id: UUID) -> Optional[OrganizationResponse]:
    organization = await get_organization_by_id(db, organization_id)
    if organization:
        return OrganizationResponse.model_validate(organization)
    return None


async def get_organizations_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[OrganizationResponse]:
    organizations = await get_organizations(db, skip, limit)
    return [OrganizationResponse.model_validate(organization) for organization in organizations]


async def get_unapproved_organizations_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[OrganizationResponse]:
    organizations = await get_unapproved_organizations(db, skip, limit)
    return [OrganizationResponse.model_validate(organization) for organization in organizations]


async def update_organization_service(db: AsyncSession, organization_id: UUID, update_data: OrganizationUpdate, updated_by: Optional[UUID] = None) -> Optional[OrganizationResponse]:
    update_dict = update_data.model_dump(exclude_unset=True)

    # Validate subscription if provided
    if "subscription_plan_id" in update_dict and update_dict["subscription_plan_id"] and not await validate_subscription_exists(db, update_dict["subscription_plan_id"]):
        raise ValueError("Invalid subscription plan ID")

    # Check email uniqueness if changing email
    if "email" in update_dict:
        existing_organization = await get_organization_by_email(db, update_dict["email"])
        if existing_organization and existing_organization.id != organization_id:
            raise ValueError("Organization email already registered")

    if updated_by:
        update_dict["updated_by"] = updated_by

    organization = await update_organization(db, organization_id, update_dict)
    if organization:
        return OrganizationResponse.model_validate(organization)
    return None


async def approve_organization_service(db: AsyncSession, organization_id: UUID, approved_by: UUID) -> Optional[OrganizationResponse]:
    return await update_organization_service(db, organization_id, OrganizationUpdate(is_approved=True), approved_by)


async def delete_organization_service(db: AsyncSession, organization_id: UUID) -> bool:
    return await delete_organization(db, organization_id)