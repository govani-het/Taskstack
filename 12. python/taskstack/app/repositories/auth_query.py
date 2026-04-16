"""Authentication query helpers."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def get_active_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get active user.
    
    Args:
        db: Database session.
        email: Email address.
    
    Returns:
        User | None: The requested resource.
    """
    stmt = (
        select(User)
        .options(selectinload(User.role))
        .where(User.email == email, User.is_active.is_(True))
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
