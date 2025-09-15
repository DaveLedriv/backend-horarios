"""add grupos table and link to clases_programadas

Revision ID: 202406010001
Revises: 202405190000
Create Date: 2024-06-01 00:00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "202406010001"
down_revision = "202405190000"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "grupos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("plan_estudio_id", sa.Integer(), nullable=False),
        sa.Column("num_estudiantes", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["plan_estudio_id"], ["planes_estudio.id"]),
    )

    op.add_column(
        "clases_programadas",
        sa.Column("grupo_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        "fk_clases_programadas_grupo_id",
        "clases_programadas",
        "grupos",
        ["grupo_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint(
        "fk_clases_programadas_grupo_id",
        "clases_programadas",
        type_="foreignkey",
    )
    op.drop_column("clases_programadas", "grupo_id")
    op.drop_table("grupos")
