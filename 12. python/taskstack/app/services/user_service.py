"""User service layer."""

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


from app.schemas.response_schemas import APIResponse
from app.constant.user_constant import (
    SUCCESS_USER_CREATED,
    SUCCESS_USER_FETCHED,
    SUCCESS_USERS_FETCHED,
    SUCCESS_USER_UPDATED,
    SUCCESS_USER_DELETED,
    ERROR_EMAIL_ALREADY_REGISTERED,
    ERROR_CANNOT_CREATE_ROLE_USER,
    ERROR_INVALID_ROLE_NAME,
    ERROR_INVALID_ORGANIZATION_NAME,
    ERROR_USER_NOT_FOUND,
    ERROR_FAILED_TO_DELETE_USER,
    ROLE_SYSTEM_ADMIN,
    ROLE_ADMIN,
)

class UserService:
    """Provides user business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def validate_role_exists(self, role_name: str) -> Optional[Role]:
        """Get a role by name for validation.

        Args:
            role_name: Role name.

        Returns:
            Optional[Role]: Matching role, if found.
        """
        return await get_role_by_name(self.db, role_name)

    async def validate_organization_exists(self, org_name: str) -> Optional[Organization]:
        """Get an organization by name for validation.

        Args:
            org_name: Organization name.

        Returns:
            Optional[Organization]: Matching organization, if found.
        """
        return await get_organization_by_name(self.db, org_name)

    async def create_user_service(self, user_data: UserCreate) -> APIResponse[UserResponse]:
        """Create a user.

        Args:
            user_data: User creation payload.

        Returns:
            APIResponse[UserResponse]: Standardized user creation response.
        """
        # Check if email already exists
        existing_user = await get_user_by_email(self.db, user_data.email)
        if existing_user:
            return APIResponse.error_response(ERROR_EMAIL_ALREADY_REGISTERED)

        # Validate role exists and get role object
        if user_data.role_name == ROLE_SYSTEM_ADMIN or user_data.role_name == ROLE_ADMIN:
            return APIResponse.error_response(ERROR_CANNOT_CREATE_ROLE_USER.format(role_name=user_data.role_name))

        role = await self.validate_role_exists(user_data.role_name)
        if not role:
            return APIResponse.error_response(ERROR_INVALID_ROLE_NAME)

        # Validate organization if provided and get organization object
        organization = None
        if user_data.organization_name:
            organization = await self.validate_organization_exists(user_data.organization_name)
            if not organization:
                return APIResponse.error_response(ERROR_INVALID_ORGANIZATION_NAME)

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

        try:
            user = await create_user(self.db, user_dict)
            return APIResponse.success_response(SUCCESS_USER_CREATED, UserResponse.model_validate(user))
        except Exception as e:
            return APIResponse.error_response(str(e))

    async def get_user_service(self, user_id: UUID) -> APIResponse[Optional[UserResponse]]:
        """Get a user by ID.

        Args:
            user_id: User identifier.

        Returns:
            APIResponse[Optional[UserResponse]]: Standardized user lookup response.
        """
        user = await get_user_by_id(self.db, user_id)
        if user:
            return APIResponse.success_response(SUCCESS_USER_FETCHED, UserResponse.model_validate(user))
        return APIResponse.error_response(ERROR_USER_NOT_FOUND)

    async def get_users_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[UserResponse]]:
        """Get users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[UserResponse]]: Standardized user list response.
        """
        users = await get_users(self.db, skip, limit)
        return APIResponse.success_response(SUCCESS_USERS_FETCHED, [UserResponse.model_validate(user) for user in users])

    async def update_user_service(self, user_id: UUID, update_data: UserUpdate, updated_by: Optional[UUID] = None) -> APIResponse[Optional[UserResponse]]:
        """Update a user.

        Args:
            user_id: User identifier.
            update_data: User update payload.
            updated_by: Identifier of the user updating the record.

        Returns:
            APIResponse[Optional[UserResponse]]: Standardized user update response.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        # Validate and convert role_name to role_id if provided
        if "role_name" in update_dict:
            role = await self.validate_role_exists(update_dict["role_name"])
            if not role:
                return APIResponse.error_response(ERROR_INVALID_ROLE_NAME)
            update_dict["role_id"] = role.id
            del update_dict["role_name"]

        # Validate and convert organization_name to organization_id if provided
        if "organization_name" in update_dict:
            if update_dict["organization_name"]:
                organization = await self.validate_organization_exists(update_dict["organization_name"])
                if not organization:
                    return APIResponse.error_response(ERROR_INVALID_ORGANIZATION_NAME)
                update_dict["organization_id"] = organization.id
            else:
                update_dict["organization_id"] = None
            del update_dict["organization_name"]

        # Check email uniqueness if changing email
        if "email" in update_dict:
            existing_user = await get_user_by_email(self.db, update_dict["email"])
            if existing_user and existing_user.id != user_id:
                return APIResponse.error_response(ERROR_EMAIL_ALREADY_REGISTERED)

        if "password" in update_dict:
            update_dict["password"] = hash_password(update_dict["password"])

        if updated_by:
            update_dict["updated_by"] = updated_by

        user = await update_user(self.db, user_id, update_dict)
        if user:
            return APIResponse.success_response(SUCCESS_USER_UPDATED, UserResponse.model_validate(user))
        return APIResponse.error_response(ERROR_USER_NOT_FOUND)

    async def delete_user_service(self, user_id: UUID, deleted_by: Optional[UUID] = None) -> APIResponse[str]:
        """Soft-delete a user.

        Args:
            user_id: User identifier.
            deleted_by: Identifier of the user deleting the record.

        Returns:
            APIResponse[str]: Standardized user deletion response.
        """
        response = await delete_user(self.db, user_id, deleted_by)
        if response:
            return APIResponse.success_response(SUCCESS_USER_DELETED)
        return APIResponse.error_response(ERROR_FAILED_TO_DELETE_USER)
