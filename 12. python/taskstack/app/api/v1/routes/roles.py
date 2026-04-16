"""Role API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.role_schemas import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_service import RoleService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.post("/", response_model=APIResponse[RoleResponse], status_code=status.HTTP_201_CREATED)
@require_roles(["system admin"])
async def create_role(
    role_data: RoleCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a role.

    Args:
        role_data: Role creation payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    role_obj = RoleService(db)
    return await role_obj.create_role_service(role_data)


@router.get("/{role_id}", response_model=APIResponse[RoleResponse])
async def get_role(
    role_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a role by ID.

    Args:
        role_id: Role identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    role_obj = RoleService(db)
    return await role_obj.get_role_service(role_id)


@router.get("/", response_model=APIResponse[List[RoleResponse]])
async def get_roles(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],    
    skip: int = 0,
    limit: int = 100,

):
    """Get roles with pagination.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    role_obj = RoleService(db)
    return await role_obj.get_roles_service(skip, limit)


@router.put("/{role_id}", response_model=APIResponse[RoleResponse])
@require_roles(["system admin"])
async def update_role(
    role_id: UUID,
    update_data: RoleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update a role.

    Args:
        role_id: Role identifier.
        update_data: Role update payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    role_obj = RoleService(db)
    return await role_obj.update_role_service(role_id, update_data, UUID(current_user["id"]))


@router.delete("/{role_id}", response_model=APIResponse[str], status_code=status.HTTP_200_OK)
@require_roles(["system admin"])
async def delete_role(
    role_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a role.

    Args:
        role_id: Role identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    role_obj = RoleService(db)
    return await role_obj.delete_role_service(role_id, UUID(current_user["id"]))
