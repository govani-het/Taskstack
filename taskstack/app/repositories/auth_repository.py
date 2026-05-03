"""Authentication repository."""

import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.password_reset_token import PasswordResetToken
from app.models.users import User
from app.repositories.audit import utc_now


async def create_password_reset_token(db: AsyncSession, user_id: UUID) -> str:
    """Create a new password reset token for the user.

    Args:
        db: Database session.
        user_id: User ID.

    Returns:
        The generated token string.
    """
    # Generate 32-character token
    token = secrets.token_hex(16)  # 32 characters

    # Set expiration to 15 minutes from now
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Create token record
    reset_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        used=False,
        created_by=user_id,
    )

    db.add(reset_token)
    await db.commit()
    await db.refresh(reset_token)

    return token


async def get_password_reset_token(db: AsyncSession, token: str) -> PasswordResetToken | None:
    """Get password reset token by token string.

    Args:
        db: Database session.
        token: Token string.

    Returns:
        PasswordResetToken if found, None otherwise.
    """
    query = select(PasswordResetToken).where(
        PasswordResetToken.token == token,
        PasswordResetToken.is_active == True,
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def mark_token_as_used(db: AsyncSession, token: str) -> None:
    """Mark a password reset token as used.

    Args:
        db: Database session.
        token: Token string.
    """
    query = select(PasswordResetToken).where(
        PasswordResetToken.token == token,
        PasswordResetToken.is_active == True,
    )
    result = await db.execute(query)
    reset_token = result.scalar_one_or_none()

    if reset_token:
        reset_token.used = True
        reset_token.updated_at = utc_now()
        reset_token.updated_by = reset_token.user_id
        await db.commit()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get user by email.

    Args:
        db: Database session.
        email: User email.

    Returns:
        User if found, None otherwise.
    """
    query = select(User).where(User.email == email, User.is_active == True)
    result = await db.execute(query)
    return result.scalar_one_or_none()
