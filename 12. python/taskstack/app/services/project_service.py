"""Project service layer."""

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
            return APIResponse.error_response("Project not found")

        if current_user.get("role") != "system admin" and str(project.organization_id) != current_user.get("organization_id"):
            return APIResponse.error_response("Access denied")

        return APIResponse.success_response("Project fetched successfully", ProjectResponse.model_validate(project))

    async def get_projects_service(self, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get projects visible to the current user.

        Args:
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectResponse]]: Standardized project list response.
        """
        if current_user.get("role") == "system admin":
            return await self.get_all_projects_service(skip, limit)

        organization_id = current_user.get("organization_id")
        if organization_id:
            return await self.get_projects_by_organization_service(UUID(organization_id), skip, limit)

        return APIResponse.error_response("No organization associated")

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
        return APIResponse.success_response("Projects fetched successfully", [ProjectResponse.model_validate(project) for project in projects])

    async def get_all_projects_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectResponse]]:
        """Get all projects.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectResponse]]: Standardized project list response.
        """
        projects = await get_all_projects(self.db, skip, limit)
        return APIResponse.success_response("All projects fetched successfully", [ProjectResponse.model_validate(project) for project in projects])
