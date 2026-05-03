"""drop ticket attachments column

Revision ID: a12b3c4d5e6f
Revises: 661a98166ed1
Create Date: 2026-04-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a12b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = '661a98166ed1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE tickets DROP COLUMN IF EXISTS attachments")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('tickets', sa.Column('attachments', sa.JSON(), nullable=True))
