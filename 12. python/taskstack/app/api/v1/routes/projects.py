"""Project API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from starlette.requests import Request

from app.config.database import get_db
from app.schemas.project_schemas import ProjectResponse, ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

from app.constant.role_constant import ROLE_SYSTEM_ADMIN,ROLE_ADMIN,ROLE_PROJECT_MANAGER

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/", response_model=APIResponse[List[ProjectResponse]])
async def get_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    
):
    """Get projects visible to the current user.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    project_obj = ProjectService(db)
    return await project_obj.get_projects_service(current_user, skip, limit)


@router.get("/all", response_model=APIResponse[List[ProjectResponse]])
@require_roles([ROLE_SYSTEM_ADMIN])
async def get_all_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    organization_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    
):
    """Get all projects or filter by organization.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        organization_id: Optional organization ID to filter projects.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    project_obj = ProjectService(db)
    if organization_id:
        return await project_obj.get_projects_by_organization_service(organization_id, skip, limit)
    else:
        return await project_obj.get_all_projects_service(skip, limit)


@router.get("/{project_id}", response_model=APIResponse[ProjectResponse])
async def get_project(
    project_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a project by ID.

    Args:
        project_id: Project identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Raises:
        HTTPException: If the project is missing or the user lacks access.
    """
    project_obj = ProjectService(db)
    return await project_obj.get_project_service(project_id, current_user)


@router.patch("/{project_id}", response_model=APIResponse[ProjectResponse])
@require_roles([ROLE_ADMIN, ROLE_PROJECT_MANAGER])
async def update_project(
        project_id: UUID,
        project_data: ProjectUpdate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update a project."""
    project_obj = ProjectService(db)
    return await project_obj.update_project_service(project_id, project_data, current_user)


@router.delete("/{project_id}", response_model=APIResponse[ProjectResponse])
@require_roles([ROLE_ADMIN])
async def delete_project(
        project_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a project."""
    project_obj = ProjectService(db)
    return await project_obj.delete_project_service(project_id, current_user)


@router.post("/", response_model=APIResponse[ProjectResponse])
@require_roles([ROLE_ADMIN, ROLE_PROJECT_MANAGER])
async def create_project(
        project_data: ProjectCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a new project.
    Args:
        db: Database session.
    """
    project_obj = ProjectService(db)
    print("Creating project with data:", project_data)
    return await project_obj.create_project_service(project_data, current_user)



