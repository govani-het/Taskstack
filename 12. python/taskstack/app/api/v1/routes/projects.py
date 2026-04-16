"""Project API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.project_schemas import ProjectResponse
from app.services.project_service import ProjectService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/all", response_model=APIResponse[List[ProjectResponse]])
@require_roles(["system admin"])
async def get_all_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    
):
    """Get all projects.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    project_obj = ProjectService(db)
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
    return await project_obj.get_project_service(project_id, current_user)


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

    Returns:
        APIResponse[List[ProjectResponse]]: Standardized project list response.
    """
    project_obj = ProjectService(db)
    return await project_obj.get_projects_service(current_user, skip, limit)
