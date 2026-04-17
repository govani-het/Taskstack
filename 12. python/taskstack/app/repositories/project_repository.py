"""Project repository functions."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.projects import Project
from app.models.project_member import ProjectMember
from app.models.users import User
from app.schemas.project_schemas import ProjectCreate


async def get_project_by_id(db: AsyncSession, project_id: UUID) -> Optional[Project]:
    """Get project.
    
    Args:
        db: Database session.
        project_id: Project identifier.
    
    Returns:
        Optional[Project]: Result of the operation.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(Project.id == project_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_projects_by_organization(db: AsyncSession, organization_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get projects by organization.
    
    Args:
        db: Database session.
        organization_id: Organization identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Project]: Result of the operation.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(Project.organization_id == organization_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get all projects.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[Project]: Result of the operation.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_project(db: AsyncSession, project_data: dict) -> Project:
    """Create a new project.

    Args:
        db: Database session.
        project_data: Project creation payload as a dict.

    Returns:
        Project: Result of the operation.
    """

    project_obj = Project(**project_data)
    db.add(project_obj)
    await db.commit()
   

    await db.refresh(project_obj, attribute_names=["organization"])

    return project_obj