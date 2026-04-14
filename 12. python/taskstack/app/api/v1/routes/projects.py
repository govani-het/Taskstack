from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.schemas.project_schemas import ProjectResponse
from app.services.project_service import (
    get_project_service,
    get_projects_by_organization_service,
    get_all_projects_service,
)
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import check_allowed_roles

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/all", response_model=List[ProjectResponse])
async def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    check_allowed_roles(current_user, ["system admin"], "view all projects")
    return await get_all_projects_service(db, skip, limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    project = await get_project_service(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Super admin can view any project, others can only view projects in their organization
    if current_user.get("role") != "system admin" and str(project.organization_id) != current_user.get("organization_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return project


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Super admin can view all projects, others can only view projects in their organization
    if current_user.get("role") == "system admin":
        return await get_all_projects_service(db, skip, limit)
    elif current_user.get("organization_id"):
        return await get_projects_by_organization_service(db, UUID(current_user["organization_id"]), skip, limit)
    else:
        return []