"""add timestamps

Revision ID: 1beda43ff58b
Revises: 5facc1ba8584
Create Date: 2025-09-11 20:10:06.944009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1beda43ff58b'
down_revision = '5facc1ba8584'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('docentes', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('docentes', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('materias', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('materias', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('asignaciones_materia', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('asignaciones_materia', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('clases_programadas', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('clases_programadas', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade():
    op.drop_column('clases_programadas', 'updated_at')
    op.drop_column('clases_programadas', 'created_at')
    op.drop_column('asignaciones_materia', 'updated_at')
    op.drop_column('asignaciones_materia', 'created_at')
    op.drop_column('materias', 'updated_at')
    op.drop_column('materias', 'created_at')
    op.drop_column('docentes', 'updated_at')
    op.drop_column('docentes', 'created_at')
