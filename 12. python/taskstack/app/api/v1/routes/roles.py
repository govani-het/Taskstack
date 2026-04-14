from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.schemas.role_schemas import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_service import (
    create_role_service,
    get_role_service,
    get_roles_service,
    update_role_service,
    delete_role_service,
)
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import check_allowed_roles

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "create roles")

    try:
        role = await create_role_service(db, role_data)
        return role
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    role = await get_role_service(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await get_roles_service(db, skip, limit)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    update_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "update roles")

    try:
        role = await update_role_service(db, role_id, update_data)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return role
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "delete roles")

    success = await delete_role_service(db, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")