"""create disponibilidad_docente table

Revision ID: 202405190001
Revises: 202405190000
Create Date: 2024-05-19 00:00:01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from app.enums import DiaSemanaEnum

# revision identifiers, used by Alembic.
revision = "202405190001"
down_revision = "202405190000"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "disponibilidad_docente" not in inspector.get_table_names():
        op.create_table(
            "disponibilidad_docente",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "docente_id",
                sa.Integer(),
                sa.ForeignKey("docentes.id"),
                nullable=False,
            ),
            sa.Column(
                "dia",
                sa.Enum(DiaSemanaEnum, name="diasemanaenum"),
                nullable=False,
            ),
            sa.Column("hora_inicio", sa.Time(), nullable=False),
            sa.Column("hora_fin", sa.Time(), nullable=False),
        )


def downgrade():
    op.drop_table("disponibilidad_docente")
