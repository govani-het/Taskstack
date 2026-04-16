"""Project member API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.project_member_schemas import ProjectMemberResponse
from app.services.project_member_service import ProjectMemberService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

router = APIRouter(
    prefix="/project-members",
    tags=["project-members"],
)


@router.get("/all", response_model=APIResponse[List[ProjectMemberResponse]])
@require_roles(["system admin"])
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
    # Check if user has access to this project
    from app.repositories.project_repository import get_project_by_id
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Super admin can view any project members, others can only view members of projects in their organization
    if current_user.get("role") != "system admin" and str(project.organization_id) != current_user.get("organization_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    member_obj = ProjectMemberService(db)
    return await member_obj.get_project_members_by_project_service(project_id, skip, limit)
