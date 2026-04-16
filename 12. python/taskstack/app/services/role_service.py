"""Role service layer."""

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


from app.schemas.response_schemas import APIResponse
from app.constant.role_constant import (
    SUCCESS_ROLE_CREATED,
    SUCCESS_ROLE_FETCHED,
    SUCCESS_ROLES_FETCHED,
    SUCCESS_ROLE_UPDATED,
    SUCCESS_ROLE_DELETED,
    ERROR_ROLE_NAME_ALREADY_EXISTS,
    ERROR_ROLE_NOT_FOUND,
    ERROR_FAILED_TO_DELETE_ROLE,
    ROLE_SYSTEM_ADMIN,
)

class RoleService:
    """Provides role business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def create_role_service(self, role_data: RoleCreate) -> APIResponse[RoleResponse]:
        """Create a role.

        Args:
            role_data: Role creation payload.

        Returns:
            APIResponse[RoleResponse]: Standardized role creation response.
        """
        # Check if role name already exists
        existing_role = await get_role_by_name(self.db, role_data.name)
        if existing_role:
            return APIResponse.error_response(ERROR_ROLE_NAME_ALREADY_EXISTS)

        role_dict = role_data.model_dump()
        try:
            role = await create_role(self.db, role_dict)
            return APIResponse.success_response(SUCCESS_ROLE_CREATED, RoleResponse.model_validate(role))
        except Exception as e:
            return APIResponse.error_response(str(e))

    async def get_role_service(self, role_id: UUID) -> APIResponse[Optional[RoleResponse]]:
        """Get a role by ID.

        Args:
            role_id: Role identifier.

        Returns:
            APIResponse[Optional[RoleResponse]]: Standardized role lookup response.
        """
        role = await get_role_by_id(self.db, role_id)
        if role:
            return APIResponse.success_response(SUCCESS_ROLE_FETCHED, RoleResponse.model_validate(role))
        return APIResponse.error_response(ERROR_ROLE_NOT_FOUND)

    async def get_roles_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[RoleResponse]]:
        """Get roles with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[RoleResponse]]: Standardized role list response.
        """
        roles = await get_roles(self.db, skip, limit)
        return APIResponse.success_response(SUCCESS_ROLES_FETCHED, [RoleResponse.model_validate(role) for role in roles])

    async def update_role_service(self, role_id: UUID, update_data: RoleUpdate, updated_by: Optional[UUID] = None) -> APIResponse[Optional[RoleResponse]]:
        """Update a role.

        Args:
            role_id: Role identifier.
            update_data: Role update payload.
            updated_by: Identifier of the user updating the record.

        Returns:
            APIResponse[Optional[RoleResponse]]: Standardized role update response.
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        # Check name uniqueness if changing name
        if "name" in update_dict:
            existing_role = await get_role_by_name(self.db, update_dict["name"])
            if existing_role and existing_role.id != role_id:
                return APIResponse.error_response(ERROR_ROLE_NAME_ALREADY_EXISTS)

        if updated_by:
            update_dict["updated_by"] = updated_by

        role = await update_role(self.db, role_id, update_dict)
        if role:
            return APIResponse.success_response(SUCCESS_ROLE_UPDATED, RoleResponse.model_validate(role))
        return APIResponse.error_response(ERROR_ROLE_NOT_FOUND)

    async def delete_role_service(self, role_id: UUID, deleted_by: Optional[UUID] = None) -> APIResponse[str]:
        """Soft-delete a role.

        Args:
            role_id: Role identifier.
            deleted_by: Identifier of the user deleting the record.

        Returns:
            APIResponse[str]: Standardized role deletion response.
        """
        response = await delete_role(self.db, role_id, deleted_by)
        if response:
            return APIResponse.success_response(SUCCESS_ROLE_DELETED)
        return APIResponse.error_response(ERROR_FAILED_TO_DELETE_ROLE)
