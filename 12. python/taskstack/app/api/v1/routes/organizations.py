"""Organization API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.organization_schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.organization_service import OrganizationService
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles
from app.schemas.response_schemas import APIResponse


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)

@router.post("/", response_model=APIResponse[OrganizationResponse], status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_data: OrganizationCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create an organization.

    Args:
        organization_data: Organization creation payload.
        db: Database session.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.create_organization_service(organization_data)


@router.get("/{organization_id}", response_model=APIResponse[OrganizationResponse])
@require_roles(["system admin"])
async def get_organization(
    organization_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get an organization by ID.

    Args:
        organization_id: Organization identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.get_organization_service(organization_id)


@router.get("/", response_model=APIResponse[List[OrganizationResponse]])
async def get_organizations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get organizations visible to the current user.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.get_organizations_service(current_user, skip, limit)


@router.get("/unapproved/", response_model=APIResponse[List[OrganizationResponse]])
@require_roles(["system admin"])
async def get_unapproved_organizations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    
):
    """Get unapproved organizations.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.get_unapproved_organizations_service(skip, limit)


@router.put("/{organization_id}", response_model=APIResponse[OrganizationResponse])
@require_roles(["system admin"])
async def update_organization(
    organization_id: UUID,
    update_data: OrganizationUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update an organization.

    Args:
        organization_id: Organization identifier.
        update_data: Organization update payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.update_organization_service(organization_id, update_data, UUID(current_user["id"]))


@router.put("/{organization_id}/approve", response_model=APIResponse[OrganizationResponse])
@require_roles(["system admin"])
async def approve_organization(
    organization_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Approve an organization.

    Args:
        organization_id: Organization identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    organization_obj = OrganizationService(db)
    response = await organization_obj.approve_organization_service(organization_id, UUID(current_user["id"]))
    if not response.data:
        return APIResponse.error_response("Organization not found")
    return response


@router.delete("/{organization_id}", response_model=APIResponse[str], status_code=status.HTTP_200_OK)
@require_roles(["system admin"])
async def delete_organization(
    organization_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete an organization.

    Args:
        organization_id: Organization identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    organization_obj = OrganizationService(db)
    return await organization_obj.delete_organization_service(organization_id, UUID(current_user["id"]))
