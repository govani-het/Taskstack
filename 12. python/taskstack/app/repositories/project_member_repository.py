"""Project member repository functions."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.project_member import ProjectMember


async def get_project_members_by_project(db: AsyncSession, project_id: UUID, skip: int = 0, limit: int = 100) -> List[ProjectMember]:
    """Get project members.
    
    Args:
        db: Database session.
        project_id: Project identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[ProjectMember]: Result of the operation.
    """
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload("role"),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.project_id == project_id, ProjectMember.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_project_members(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProjectMember]:
    """Get all project members.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[ProjectMember]: Result of the operation.
    """
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload("role"),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project).selectinload("organization"),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
