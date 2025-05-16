"""phone number

Revision ID: 5c2eeb654168
Revises: cc193d7e9e8f
Create Date: 2025-05-02 15:59:40.857596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c2eeb654168'
down_revision: Union[str, None] = 'cc193d7e9e8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))



def downgrade() -> None:
    pass
