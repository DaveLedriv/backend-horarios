"""add aula model

Revision ID: 5facc1ba8584
Revises: 
Create Date: 2025-09-07 05:19:42.429139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5facc1ba8584'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'aulas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=100), nullable=False, unique=True),
        sa.Column('capacidad', sa.Integer(), nullable=True),
    )
    op.add_column('clases_programadas', sa.Column('aula_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_clases_programadas_aula_id',
        'clases_programadas',
        'aulas',
        ['aula_id'],
        ['id'],
    )
    op.drop_column('clases_programadas', 'aula')


def downgrade():
    op.add_column('clases_programadas', sa.Column('aula', sa.String(), nullable=False))
    op.drop_constraint('fk_clases_programadas_aula_id', 'clases_programadas', type_='foreignkey')
    op.drop_column('clases_programadas', 'aula_id')
    op.drop_table('aulas')
