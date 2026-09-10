"""empty message

Revision ID: 3e60d26469c7
Revises: 
Create Date: 2026-09-10 23:01:47.910413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e60d26469c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", 
                    "password_hash", 
                    existing_type=sa.String(length=50),
                    type_=sa.String(length=255)
    )


def downgrade() -> None:
    op.alter_column("users", 
                    "password_hash", 
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=50)
    )
