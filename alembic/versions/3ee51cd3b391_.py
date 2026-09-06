"""empty message

Revision ID: 3ee51cd3b391
Revises: 
Create Date: 2026-09-06 22:53:15.291512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ee51cd3b391'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('priority', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'priority')
