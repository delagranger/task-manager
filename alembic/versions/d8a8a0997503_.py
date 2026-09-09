"""empty message

Revision ID: d8a8a0997503
Revises: 3ee51cd3b391
Create Date: 2026-09-07 10:26:22.835595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8a8a0997503'
down_revision: Union[str, Sequence[str], None] = '3ee51cd3b391'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('deadline', sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'deadline')
