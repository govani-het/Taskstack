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
    remove_project_member,
    update_project_member,
)
from app.repositories.project_repository import get_project_by_id
from app.repositories.user_repository import get_user_by_id
from app.repositories.role_repository import get_role_by_id
from app.schemas.project_member_schemas import ProjectMemberResponse, UpdateProjectMemberRole


from app.schemas.response_schemas import APIResponse
from app.constant.project_member_constant import (
    ROLE_SYSTEM_ADMIN,
)
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_PROJECT_MANAGER,
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
        
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        if project.organization_id != UUID(current_user.get("organization_id")):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot add a member to a project that belongs to another organization.")

        
        user = await get_user_by_id(self.db, project_member_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        
        if user.organization_id != project.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User must belong to the same organization as the project"
            )

        
        role = await get_role_by_id(self.db, project_member_data.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        
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
            
            update_data = {"is_active": True}
            reactivated_member = await update_project_member(
                self.db, 
                existing_member, 
                update_data,
                UUID(current_user.get("id"))
            )
            return APIResponse.success_response(
                "Project member added successfully",
                ProjectMemberResponse.model_validate(reactivated_member)
            )

        
        member_data = {
            "project_id": project_id,
            "user_id": project_member_data.user_id,
            "role_id": project_member_data.role_id,
            "project_manager_id": project_member_data.project_manager_id,
            "is_active": True,
            "created_by": UUID(current_user.get("id")),
        }

        new_member = await create_project_member(self.db, member_data)

        return APIResponse.success_response(
            "Project member added successfully",
            ProjectMemberResponse.model_validate(new_member)
        )


    async def remove_project_member_service(self, project_member, project_id, current_user):
        """Remove a member from a project.
        
        Args:
            project_member: Project member data from request.
            project_id: Project identifier.
            current_user: Authenticated user payload.
        
        Returns:
            APIResponse[ProjectMemberResponse]: Standardized project-member removal response.
        
        Raises:
            HTTPException: If validation fails.
        """

        
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        if project.organization_id != UUID(current_user.get("organization_id")) or current_user.get("role") not in [
            "admin", "project_manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to remove members from this project."
            )

        user = await get_user_by_id(self.db, project_member.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        
        existing_member = await get_project_member_by_user_and_project(
            self.db,
            project_member.user_id,
            project_id
        )
        if not existing_member or not existing_member.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not an active member of this project"
            )

       
        removed_member = await remove_project_member(
            self.db,
            existing_member,
            UUID(current_user.get("id"))
        )

        return APIResponse.success_response(
            "Project member removed successfully",
            ProjectMemberResponse.model_validate(removed_member)
        )

    async def update_project_member_role_service(self, project_member_data: UpdateProjectMemberRole, project_id: UUID, member_id: UUID, current_user: dict) -> APIResponse[ProjectMemberResponse]:
        """Update a project member's role.

        Args:
            project_member_data: UpdateProjectMemberRole payload containing new role_id.
            project_id: Project identifier.
            member_id: Project member identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[ProjectMemberResponse]: Standardized project-member update response.

        Raises:
            HTTPException: If validation fails or user lacks permission.
        """
        # Verify project exists and belongs to the current user's organization
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        if project.organization_id != UUID(current_user.get("organization_id")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update members of a project that belongs to another organization."
            )

        # Check if current user has permission to update roles (only admin and project manager)
        if current_user.get("role") not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins and project managers can update project member roles."
            )

        # Verify the new role exists
        new_role = await get_role_by_id(self.db, project_member_data.role_id)
        if not new_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New role not found"
            )

        # Get the project member to update
        existing_member = await get_project_member_by_user_and_project(
            self.db,
            member_id,
            project_id
        )
        if not existing_member or not existing_member.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project member not found or inactive"
            )

        # Update the member's role
        update_data = {"role_id": project_member_data.role_id}
        updated_member = await update_project_member(
            self.db,
            existing_member,
            update_data,
            UUID(current_user.get("id"))
        )

        return APIResponse.success_response(
            "Project member role updated successfully",
            ProjectMemberResponse.model_validate(updated_member)
        )