from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.projects import Project


async def get_project_by_id(db: AsyncSession, project_id: UUID) -> Optional[Project]:
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload("user").selectinload("role"),
            selectinload(Project.members).selectinload("role")
        )
        .where(Project.id == project_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_projects_by_organization(db: AsyncSession, organization_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload("user").selectinload("role"),
            selectinload(Project.members).selectinload("role")
        )
        .where(Project.organization_id == organization_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload("user").selectinload("role"),
            selectinload(Project.members).selectinload("role")
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()