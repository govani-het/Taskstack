from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.repositories.role_repository import (
    get_role_by_id,
    get_role_by_name,
    get_roles,
    create_role,
    update_role,
    delete_role,
)
from app.schemas.role_schemas import RoleCreate, RoleUpdate, RoleResponse


async def create_role_service(db: AsyncSession, role_data: RoleCreate) -> RoleResponse:
    # Check if role name already exists
    existing_role = await get_role_by_name(db, role_data.name)
    if existing_role:
        raise ValueError("Role name already exists")

    role_dict = role_data.model_dump()
    role = await create_role(db, role_dict)
    return RoleResponse.model_validate(role)


async def get_role_service(db: AsyncSession, role_id: UUID) -> Optional[RoleResponse]:
    role = await get_role_by_id(db, role_id)
    if role:
        return RoleResponse.model_validate(role)
    return None


async def get_roles_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
    roles = await get_roles(db, skip, limit)
    return [RoleResponse.model_validate(role) for role in roles]


async def update_role_service(db: AsyncSession, role_id: UUID, update_data: RoleUpdate) -> Optional[RoleResponse]:
    update_dict = update_data.model_dump(exclude_unset=True)

    # Check name uniqueness if changing name
    if "name" in update_dict:
        existing_role = await get_role_by_name(db, update_dict["name"])
        if existing_role and existing_role.id != role_id:
            raise ValueError("Role name already exists")

    role = await update_role(db, role_id, update_dict)
    if role:
        return RoleResponse.model_validate(role)
    return None


async def delete_role_service(db: AsyncSession, role_id: UUID) -> bool:
    return await delete_role(db, role_id)