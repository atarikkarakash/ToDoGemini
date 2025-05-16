"""phone number added

Revision ID: cc193d7e9e8f
Revises: 
Create Date: 2025-05-02 15:43:47.714524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc193d7e9e8f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('owner_id', sa.Integer(), nullable=False))


def downgrade() -> None:
    pass
