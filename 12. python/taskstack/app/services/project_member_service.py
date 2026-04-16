"""Project member service layer."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.repositories.project_member_repository import (
    get_project_members_by_project,
    get_all_project_members,
)
from app.repositories.project_repository import get_project_by_id
from app.schemas.project_member_schemas import ProjectMemberResponse


from app.schemas.response_schemas import APIResponse
from app.constant.project_member_constant import (
    ROLE_SYSTEM_ADMIN,
)

class ProjectMemberService:
    """Provides project member business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def get_project_members_by_project_service(self, project_id: UUID, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectMemberResponse]]:
        """Get members for a project.

        Args:
            project_id: Project identifier.
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectMemberResponse]]: Standardized project-member list response.
        """
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        if current_user.get("role") != ROLE_SYSTEM_ADMIN and str(project.organization_id) != current_user.get("organization_id"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        members = await get_project_members_by_project(self.db, project_id, skip, limit)
        if not members:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project member not found")
        return APIResponse.success_response(
            "Project members fetched successfully",
            [ProjectMemberResponse.model_validate(member) for member in members]
        )

    async def get_all_project_members_service(self, skip: int = 0, limit: int = 100) -> APIResponse[List[ProjectMemberResponse]]:
        """Get all project members.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ProjectMemberResponse]]: Standardized project-member list response.
        """
        members = await get_all_project_members(self.db, skip, limit)
        return APIResponse.success_response("All project members fetched successfully", [ProjectMemberResponse.model_validate(member) for member in members])
