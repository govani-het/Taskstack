"""add audit fields to password reset tokens

Revision ID: 4f0a9c2b7d11
Revises: 3513096ad668
Create Date: 2026-05-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f0a9c2b7d11"
down_revision: Union[str, Sequence[str], None] = "3513096ad668"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "password_reset_tokens",
        sa.Column("created_by", sa.UUID(), nullable=True),
    )
    op.add_column(
        "password_reset_tokens",
        sa.Column("updated_by", sa.UUID(), nullable=True),
    )
    op.add_column(
        "password_reset_tokens",
        sa.Column("deleted_by", sa.UUID(), nullable=True),
    )
    op.add_column(
        "password_reset_tokens",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "password_reset_tokens",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.create_foreign_key(
        "fk_password_reset_tokens_created_by_users",
        "password_reset_tokens",
        "users",
        ["created_by"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_password_reset_tokens_updated_by_users",
        "password_reset_tokens",
        "users",
        ["updated_by"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_password_reset_tokens_deleted_by_users",
        "password_reset_tokens",
        "users",
        ["deleted_by"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_password_reset_tokens_deleted_by_users",
        "password_reset_tokens",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_password_reset_tokens_updated_by_users",
        "password_reset_tokens",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_password_reset_tokens_created_by_users",
        "password_reset_tokens",
        type_="foreignkey",
    )
    op.drop_column("password_reset_tokens", "is_active")
    op.drop_column("password_reset_tokens", "deleted_at")
    op.drop_column("password_reset_tokens", "deleted_by")
    op.drop_column("password_reset_tokens", "updated_by")
    op.drop_column("password_reset_tokens", "created_by")
