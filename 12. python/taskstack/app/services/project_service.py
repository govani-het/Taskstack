"""Project service layer."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.repositories.project_repository import (
    get_project_by_id,
    get_projects_by_organization,
    get_all_projects,
)
from app.schemas.project_schemas import ProjectResponse


from app.schemas.response_schemas import APIResponse
from app.constant.project_constant import (
    SUCCESS_PROJECT_FETCHED,
    SUCCESS_PROJECTS_FETCHED,
    SUCCESS_ALL_PROJECTS_FETCHED,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_ACCESS_DENIED,
    ERROR_NO_ORGANIZATION_ASSOCIATED,
    ROLE_SYSTEM_ADMIN,
)

class ProjectService:
    """Provides project business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

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

        if current_user.get("role") != ROLE_SYSTEM_ADMIN and str(project.organization_id) != current_user.get("organization_id"):
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
        if current_user.get("role") == ROLE_SYSTEM_ADMIN:
            return await self.get_all_projects_service(skip, limit)

        organization_id = current_user.get("organization_id")
        if organization_id:
            return await self.get_projects_by_organization_service(UUID(organization_id), skip, limit)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_NO_ORGANIZATION_ASSOCIATED)

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
        return APIResponse.success_response(SUCCESS_PROJECTS_FETCHED, [ProjectResponse.model_validate(project) for project in projects])

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
