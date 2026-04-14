from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.schemas.organization_schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.organization_service import (
    create_organization_service,
    get_organization_service,
    get_organizations_service,
    get_unapproved_organizations_service,
    update_organization_service,
    approve_organization_service,
    delete_organization_service,
)
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import check_allowed_roles

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        organization = await create_organization_service(db, organization_data)
        return organization
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Super admin can view any organization, others can only view their own
    if current_user.get("role") != "system admin" and str(organization_id) != current_user.get("organization_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    organization = await get_organization_service(db, organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return organization


@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Super admin can view all organizations, others can only view their own
    if current_user.get("role") == "system admin":
        return await get_organizations_service(db, skip, limit)
    else:
        # For non-super admin, return only their organization
        if current_user.get("organization_id"):
            organization = await get_organization_service(db, UUID(current_user["organization_id"]))
            return [organization] if organization else []
        else:
            return []


@router.get("/unapproved/", response_model=List[OrganizationResponse])
async def get_unapproved_organizations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "view unapproved organizations")
    return await get_unapproved_organizations_service(db, skip, limit)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    update_data: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Super admin can update any organization, others can only update their own
    if current_user.get("role") != "system admin" and str(organization_id) != current_user.get("organization_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        organization = await update_organization_service(db, organization_id, update_data, UUID(current_user["id"]))
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        return organization
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{organization_id}/approve", response_model=OrganizationResponse)
async def approve_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "approve organizations")
    organization = await approve_organization_service(db, organization_id, UUID(current_user["id"]))
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["admin"], "delete organizations")

    success = await delete_organization_service(db, organization_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")