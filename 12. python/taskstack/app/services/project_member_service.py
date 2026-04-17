"""Project member service layer."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models import ProjectMember
from app.repositories.project_member_repository import (
    get_project_members_by_project,
    get_all_project_members,
    create_project_member,
    get_project_member_by_user_and_project,
)
from app.repositories.project_repository import get_project_by_id
from app.repositories.user_repository import get_user_by_id
from app.repositories.role_repository import get_role_by_id
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

    async def add_project_member_service(self, project_member_data, project_id, current_user) -> APIResponse[ProjectMemberResponse]:
        """Add a member to a project.

        Args:
            project_member_data: ProjectMember creation payload.
            project_id: Project identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[ProjectMemberResponse]: Standardized project-member creation response.

        Raises:
            HTTPException: If validation fails.
        """
        # Verify project exists and belongs to the current user's organization
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        print("???????????????????????????????????????")
        print(type(project.organization_id))
        print(type(current_user.get("organization_id")))

        if project.organization_id != UUID(current_user.get("organization_id")):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot add a member to a project that belongs to another organization.")

        # Verify user exists
        user = await get_user_by_id(self.db, project_member_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify user belongs to the same organization as the project
        if user.organization_id != project.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User must belong to the same organization as the project"
            )

        # Verify role exists
        role = await get_role_by_id(self.db, project_member_data.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        # Check if user is already a member of this project
        existing_member = await get_project_member_by_user_and_project(
            self.db,
            project_member_data.user_id,
            project_id
        )
        if existing_member:
            if existing_member.is_active:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already a member of this project"
                )
            # If they were a member but left, reactivate them
            existing_member.is_active = True
            self.db.add(existing_member)
            await self.db.commit()
            await self.db.refresh(existing_member)
            return APIResponse.success_response(
                "Project member added successfully",
                ProjectMemberResponse.model_validate(existing_member)
            )

        # Create new project member
        member_data = {
            "project_id": project_id,
            "user_id": project_member_data.user_id,
            "role_id": project_member_data.role_id,
            "project_manager_id": project_member_data.project_manager_id,
            "is_active": True,
        }

        new_member = await create_project_member(self.db, member_data)

        return APIResponse.success_response(
            "Project member added successfully",
            ProjectMemberResponse.model_validate(new_member)
        )


