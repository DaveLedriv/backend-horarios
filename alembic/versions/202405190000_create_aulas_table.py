"""create aulas table

Revision ID: 202405190000
Revises: 9f88e3c56905
Create Date: 2024-05-19 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "202405190000"
down_revision = "9f88e3c56905"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "aulas" not in inspector.get_table_names():
        op.create_table(
            "aulas",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("nombre", sa.String(length=100), nullable=False, unique=True),
            sa.Column("capacidad", sa.Integer(), nullable=False),
        )


def downgrade():
    op.drop_table("aulas")
