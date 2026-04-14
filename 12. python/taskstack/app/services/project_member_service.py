from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.repositories.project_member_repository import (
    get_project_members_by_project,
    get_all_project_members,
)
from app.schemas.project_member_schemas import ProjectMemberResponse


async def get_project_members_by_project_service(db: AsyncSession, project_id: UUID, skip: int = 0, limit: int = 100) -> List[ProjectMemberResponse]:
    members = await get_project_members_by_project(db, project_id, skip, limit)
    return [ProjectMemberResponse.model_validate(member) for member in members]


async def get_all_project_members_service(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProjectMemberResponse]:
    members = await get_all_project_members(db, skip, limit)
    return [ProjectMemberResponse.model_validate(member) for member in members]