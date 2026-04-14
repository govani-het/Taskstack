from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.repositories.project_repository import (
    get_project_by_id,
    get_projects_by_organization,
    get_all_projects,
)
from app.schemas.project_schemas import ProjectResponse


async def get_project_service(db: AsyncSession, project_id: UUID) -> Optional[ProjectResponse]:
    project = await get_project_by_id(db, project_id)
    if project:
        return ProjectResponse.model_validate(project)
    return None


async def get_projects_by_organization_service(db: AsyncSession, organization_id: UUID, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
    projects = await get_projects_by_organization(db, organization_id, skip, limit)
    return [ProjectResponse.model_validate(project) for project in projects]


async def get_all_projects_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
    projects = await get_all_projects(db, skip, limit)
    return [ProjectResponse.model_validate(project) for project in projects]