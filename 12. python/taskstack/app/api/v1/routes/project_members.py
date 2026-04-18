"""Project member API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.models import ProjectMember
from app.schemas.project_member_schemas import ProjectMemberResponse, ProjectMemberBase, RemoveProjectMember, UpdateProjectMemberRole
from app.services.project_member_service import ProjectMemberService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles
from app.constant.role_constant import ROLE_SYSTEM_ADMIN, ROLE_ADMIN, ROLE_PROJECT_MANAGER
from app.services.project_member_service import ProjectMemberService
from app.schemas.project_member_schemas import RemoveProjectMember


router = APIRouter(
    prefix="/project-members",
    tags=["project-members"],
)


@router.get("/all", response_model=APIResponse[List[ProjectMemberResponse]])
@require_roles([ROLE_SYSTEM_ADMIN])
async def get_all_project_members(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    
):
    """Get all project members.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    member_obj = ProjectMemberService(db)
    return await member_obj.get_all_project_members_service(skip, limit)


@router.get("/project/{project_id}", response_model=APIResponse[List[ProjectMemberResponse]])
@require_roles([ROLE_SYSTEM_ADMIN])
async def get_project_members(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    project_id: UUID,
    skip: int = 0,
    limit: int = 100,
    
):
    """Get members for a specific project.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        project_id: Project identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Raises:
        HTTPException: If the project is missing or the user lacks access.
    """
    member_obj = ProjectMemberService(db)
    return await member_obj.get_project_members_by_project_service(project_id, current_user, skip, limit)


@router.post("/project/{project_id}", response_model=APIResponse[ProjectMemberResponse])
@require_roles([ROLE_ADMIN])
async def create_project_member(
        project_memeber: ProjectMemberBase,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
        project_id: UUID,
):
    """Create a new project member.
    Args:
        project_memeber: Project member creation payload.
        db: Database session.
        current_user: Authenticated user payload.
        project_id: Project identifier.
    
    Returns:
        APIResponse[ProjectMemberResponse]: Project member creation response.
    """
    project_member_obj = ProjectMemberService(db)
    return await project_member_obj.add_project_member_service(project_memeber, project_id, current_user)

@router.delete("/project/{project_id}")
@require_roles([ROLE_ADMIN,ROLE_PROJECT_MANAGER])
async def remove_project_member(
        project_member: RemoveProjectMember,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
        project_id: UUID,
):
    project_member_obj = ProjectMemberService(db)
    return await project_member_obj.remove_project_member_service(project_member, project_id, current_user)


@router.patch("/project/{project_id}/member/{member_id}", response_model=APIResponse[ProjectMemberResponse])
@require_roles([ROLE_ADMIN, ROLE_PROJECT_MANAGER])
async def update_project_member_role(
        project_member_data: UpdateProjectMemberRole,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
        project_id: UUID,
        member_id: UUID,
):
    """Update a project member's role.

    Args:
        project_member_data: UpdateProjectMemberRole payload containing new role_id.
        db: Database session.
        current_user: Authenticated user payload.
        project_id: Project identifier.
        member_id: Project member identifier (user_id).

    Returns:
        APIResponse[ProjectMemberResponse]: Project member update response.
    """
    project_member_obj = ProjectMemberService(db)
    return await project_member_obj.update_project_member_role_service(
        project_member_data, project_id, member_id, current_user
    )