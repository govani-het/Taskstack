from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.refresh_token import RefreshToken


async def get_valid_refresh_token(db: AsyncSession, user_id: UUID) -> RefreshToken | None:
    stmt = (
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False, RefreshToken.expires_at > datetime.utcnow())
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_refresh_token_db(db: AsyncSession, user_id: UUID, token: str, expires_at: datetime) -> RefreshToken:
    new_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)
    return new_token


async def revoke_refresh_tokens_by_user(db: AsyncSession, user_id: UUID):
    stmt = select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
    result = await db.execute(stmt)
    tokens = result.scalars().all()
    for token in tokens:
        token.is_revoked = True
    await db.commit()
