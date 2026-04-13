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
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.models.roles import Role
from app.models.organization import Organization


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def validate_role_exists(db: AsyncSession, role_id: UUID) -> bool:
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def validate_organization_exists(db: AsyncSession, org_id: UUID) -> bool:
    stmt = select(Organization).where(Organization.id == org_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def create_user_service(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    # Check if email already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Email already registered")

    # Validate role exists
    if not await validate_role_exists(db, user_data.role_id):
        raise ValueError("Invalid role ID")

    # Validate organization if provided
    if user_data.organization_id and not await validate_organization_exists(db, user_data.organization_id):
        raise ValueError("Invalid organization ID")

    # Hash password
    hashed_password = hash_password(user_data.password)

    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_password

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

    # Validate role if provided
    if "role_id" in update_dict and not await validate_role_exists(db, update_dict["role_id"]):
        raise ValueError("Invalid role ID")

    # Validate organization if provided
    if "organization_id" in update_dict and update_dict["organization_id"] and not await validate_organization_exists(db, update_dict["organization_id"]):
        raise ValueError("Invalid organization ID")

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