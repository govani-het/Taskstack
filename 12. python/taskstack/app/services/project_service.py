"""Project service layer."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.repositories.project_repository import (
    get_project_by_id,
    get_projects_by_organization,
    get_projects_by_member,
    get_project_by_id_for_member,
    get_all_projects,
    create_project,
    update_project,
    delete_project,
)
from app.repositories.project_member_repository import get_project_member_by_user_and_project
from app.schemas.project_schemas import ProjectResponse, ProjectCreate, ProjectUpdate

from app.schemas.response_schemas import APIResponse
from app.constant.project_constant import (
    SUCCESS_PROJECT_FETCHED,
    SUCCESS_PROJECTS_FETCHED,
    SUCCESS_PROJECT_CREATED,
    SUCCESS_ALL_PROJECTS_FETCHED,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_ACCESS_DENIED,
    ERROR_NO_ORGANIZATION_ASSOCIATED,
    ROLE_SYSTEM_ADMIN,
)
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_PROJECT_MANAGER,
)

class ProjectService:
    """Provides project business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def _check_subscription_edit_access(self, organization_id: UUID) -> None:
        """Check if organization has active subscriptions that allow editing.

        Args:
            organization_id: Organization identifier.

        Raises:
            HTTPException: If editing is not allowed.
        """
        from app.services.organization_subscription_service import OrganizationSubscriptionService

        subscription_service = OrganizationSubscriptionService(self.db)
        has_access = await subscription_service.check_subscription_access(organization_id)
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Active subscription required to modify projects"
            )

    async def get_project_service(self, project_id: UUID, current_user: dict) -> APIResponse[Optional[ProjectResponse]]:
        """Get a project by ID.

        Args:
            project_id: Project identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[Optional[ProjectResponse]]: Standardized project lookup response.
        """
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND)

        role = current_user.get("role")
        if role == ROLE_SYSTEM_ADMIN:
            return APIResponse.success_response(SUCCESS_PROJECT_FETCHED, ProjectResponse.model_validate(project))

        if role == ROLE_ADMIN or role == ROLE_PROJECT_MANAGER:
            if str(project.organization_id) != current_user.get("organization_id"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)
            return APIResponse.success_response(SUCCESS_PROJECT_FETCHED, ProjectResponse.model_validate(project))

        project_member = await get_project_member_by_user_and_project(self.db, UUID(current_user.get("id")), project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)

        return APIResponse.success_response(SUCCESS_PROJECT_FETCHED, ProjectResponse.model_validate(project))

    async def get_projects_service(self, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get projects visible to the current user.

        Args:
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectResponse]]: Standardized project list response.
        """
        role = current_user.get("role")

        if role == ROLE_SYSTEM_ADMIN:
            return await self.get_all_projects_service(skip, limit)

        if role in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            organization_id = current_user.get("organization_id")
            if organization_id:
                return await self.get_projects_by_organization_service(UUID(organization_id), skip, limit)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_NO_ORGANIZATION_ASSOCIATED)

        # Developers and other roles only see projects where they are assigned
        return await self.get_projects_by_member_service(UUID(current_user.get("id")), skip, limit)

    async def get_projects_by_member_service(self, user_id: UUID, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get projects assigned to a specific user."""
        projects = await get_projects_by_member(self.db, user_id, skip, limit)
        return APIResponse.success_response(SUCCESS_PROJECTS_FETCHED, [ProjectResponse.model_validate(project) for project in projects])

    async def get_projects_by_organization_service(self, organization_id: UUID, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get projects for an organization.

        Args:
            organization_id: Organization identifier.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectResponse]]: Standardized project list response.
        """

        projects = await get_projects_by_organization(self.db, organization_id, skip, limit)
        if projects:
            return APIResponse.success_response(SUCCESS_PROJECTS_FETCHED, [ProjectResponse.model_validate(project) for project in projects])
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND)

    async def get_all_projects_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get all projects.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectResponse]]: Standardized project list response.
        """
        projects = await get_all_projects(self.db, skip, limit)
        return APIResponse.success_response(SUCCESS_ALL_PROJECTS_FETCHED, [ProjectResponse.model_validate(project) for project in projects])

    async def update_project_service(self, project_id: UUID, project_data: ProjectUpdate, current_user: dict) -> APIResponse[ProjectResponse]:
        """Update a project with role-based access control."""
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND)

        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        # Check subscription access for editing
        await self._check_subscription_edit_access(UUID(organization_id))

        if role == ROLE_SYSTEM_ADMIN:
            pass
        elif role == ROLE_ADMIN:
            if str(project.organization_id) != organization_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)
        elif role == ROLE_PROJECT_MANAGER:
            if str(project.organization_id) != organization_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)

            project_member = await get_project_member_by_user_and_project(self.db, user_id, project_id)
            if not project_member or not project_member.is_active:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)

        update_payload = project_data.model_dump(exclude_none=True)
        if role != ROLE_SYSTEM_ADMIN and "organization_id" in update_payload:
            update_payload.pop("organization_id")

        updated_project = await update_project(self.db, project, update_payload, user_id)
        return APIResponse.success_response(SUCCESS_PROJECT_FETCHED, ProjectResponse.model_validate(updated_project))

    async def delete_project_service(self, project_id: UUID, current_user: dict) -> APIResponse[ProjectResponse]:
        """Delete a project with role-based access control."""
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND)

        role = current_user.get("role")
        organization_id = current_user.get("organization_id")
        user_id = UUID(current_user.get("id"))

        # Check subscription access for editing
        await self._check_subscription_edit_access(UUID(organization_id))

        if role == ROLE_ADMIN:
            if str(project.organization_id) != organization_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_ACCESS_DENIED)

        deleted_project = await delete_project(self.db, project, user_id)
        return APIResponse.success_response(SUCCESS_PROJECT_FETCHED, ProjectResponse.model_validate(deleted_project))

    async def create_project_service(self, project_data: ProjectCreate, current_user: dict) -> APIResponse[Optional[ProjectResponse]]:
        """Create a new project.
        Args:
            current_user: Authenticated user payload.
        """
        from app.services.organization_subscription_service import OrganizationSubscriptionService

        organization_id = current_user.get("organization_id")
        if not organization_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User must be associated with an organization")

        # Check subscription access and limits
        subscription_service = OrganizationSubscriptionService(self.db)
        has_access = await subscription_service.check_subscription_access(UUID(organization_id))
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Active subscription required to create projects"
            )

        can_create = await subscription_service.check_project_creation_limit(UUID(organization_id))
        if not can_create:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project creation limit reached for current subscription plan(s)"
            )

        project_data_obj = project_data.model_dump()
        project_data_obj["organization_id"] = organization_id
        project_data_obj['created_by'] = current_user.get("id")

        try:
            response = await create_project(self.db, project_data_obj)
            if response:
                return APIResponse.success_response(SUCCESS_PROJECT_CREATED, ProjectResponse.model_validate(response))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def _check_subscription_edit_access(self, organization_id: UUID):
        """Check if organization has active subscriptions for editing operations.

        Args:
            organization_id: Organization identifier.

        Raises:
            HTTPException: If no active subscriptions found.
        """
        from app.services.organization_subscription_service import OrganizationSubscriptionService

        subscription_service = OrganizationSubscriptionService(self.db)
        has_access = await subscription_service.check_subscription_access(organization_id)
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Active subscription required to modify projects"
            )