"""add attribute created_at

Revision ID: f6ef5c209e5f
Revises: e1f9001d0af8
Create Date: 2025-08-07 15:36:41.920794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6ef5c209e5f"
down_revision: Union[str, Sequence[str], None] = "e1f9001d0af8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
