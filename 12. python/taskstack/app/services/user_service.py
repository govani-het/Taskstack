import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.repositories.user_repository import (
    get_user_by_id,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
    delete_user,
)
from app.repositories.role_repository import get_role_by_name
from app.repositories.organization_repository import get_organization_by_name
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.models.roles import Role
from app.models.organization import Organization
from app.utils.hash_password import hash_password


async def validate_role_exists(db: AsyncSession, role_name: str) -> Optional[Role]:
    return await get_role_by_name(db, role_name)


async def validate_organization_exists(db: AsyncSession, org_name: str) -> Optional[Organization]:
    return await get_organization_by_name(db, org_name)


async def create_user_service(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    # Check if email already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Email already registered")

    # Validate role exists and get role object
    role = await validate_role_exists(db, user_data.role_name)
    if not role:
        raise ValueError("Invalid role name")

    # Validate organization if provided and get organization object
    organization = None
    if user_data.organization_name:
        organization = await validate_organization_exists(db, user_data.organization_name)
        if not organization:
            raise ValueError("Invalid organization name")

    # Hash password
    hashed_password = hash_password(user_data.password)

    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_password
    user_dict["role_id"] = role.id
    user_dict.pop("role_name", None)
    user_dict.pop("organization_name", None)
    if organization:
        user_dict["organization_id"] = organization.id
    else:
        user_dict.pop("organization_id", None)

    user = await create_user(db, user_dict)
    return UserResponse.model_validate(user)


async def get_user_service(db: AsyncSession, user_id: UUID) -> Optional[UserResponse]:
    user = await get_user_by_id(db, user_id)
    if user:
        return UserResponse.model_validate(user)
    return None


async def get_users_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserResponse]:
    users = await get_users(db, skip, limit)
    return [UserResponse.model_validate(user) for user in users]


async def update_user_service(db: AsyncSession, user_id: UUID, update_data: UserUpdate) -> Optional[UserResponse]:
    update_dict = update_data.model_dump(exclude_unset=True)

    # Validate and convert role_name to role_id if provided
    if "role_name" in update_dict:
        role = await validate_role_exists(db, update_dict["role_name"])
        if not role:
            raise ValueError("Invalid role name")
        update_dict["role_id"] = role.id
        del update_dict["role_name"]

    # Validate and convert organization_name to organization_id if provided
    if "organization_name" in update_dict:
        if update_dict["organization_name"]:
            organization = await validate_organization_exists(db, update_dict["organization_name"])
            if not organization:
                raise ValueError("Invalid organization name")
            update_dict["organization_id"] = organization.id
        else:
            update_dict["organization_id"] = None
        del update_dict["organization_name"]

    # Check email uniqueness if changing email
    if "email" in update_dict:
        existing_user = await get_user_by_email(db, update_dict["email"])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

    if "password" in update_dict:
        update_dict["password"] = hash_password(update_dict["password"])

    user = await update_user(db, user_id, update_dict)
    if user:
        return UserResponse.model_validate(user)
    return None


async def delete_user_service(db: AsyncSession, user_id: UUID) -> bool:
    return await delete_user(db, user_id)