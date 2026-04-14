from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.schemas.project_member_schemas import ProjectMemberResponse
from app.services.project_member_service import (
    get_project_members_by_project_service,
    get_all_project_members_service,
)
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import check_allowed_roles

router = APIRouter(
    prefix="/project-members",
    tags=["project-members"],
)


@router.get("/all", response_model=List[ProjectMemberResponse])
async def get_all_project_members(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "view all project members")
    return await get_all_project_members_service(db, skip, limit)


@router.get("/project/{project_id}", response_model=List[ProjectMemberResponse])
async def get_project_members(
    project_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
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

    return await get_project_members_by_project_service(db, project_id, skip, limit)