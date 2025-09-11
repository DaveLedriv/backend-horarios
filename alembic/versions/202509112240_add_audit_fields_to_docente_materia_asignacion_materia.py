"""add audit fields to docente materia asignacion_materia

Revision ID: 9f88e3c56905
Revises: 5facc1ba8584
Create Date: 2025-09-11 22:40:59.170777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f88e3c56905'
down_revision = '5facc1ba8584'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'docentes',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )
    op.add_column(
        'docentes',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )

    op.add_column(
        'materias',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )
    op.add_column(
        'materias',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )

    op.add_column(
        'asignaciones_materia',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )
    op.add_column(
        'asignaciones_materia',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

    op.execute(
        """
        CREATE TRIGGER update_docentes_updated_at
        BEFORE UPDATE ON docentes
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )
    op.execute(
        """
        CREATE TRIGGER update_materias_updated_at
        BEFORE UPDATE ON materias
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )
    op.execute(
        """
        CREATE TRIGGER update_asignaciones_materia_updated_at
        BEFORE UPDATE ON asignaciones_materia
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def downgrade():
    op.execute(
        "DROP TRIGGER IF EXISTS update_asignaciones_materia_updated_at ON asignaciones_materia;"
    )
    op.execute(
        "DROP TRIGGER IF EXISTS update_materias_updated_at ON materias;"
    )
    op.execute(
        "DROP TRIGGER IF EXISTS update_docentes_updated_at ON docentes;"
    )
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")

    op.drop_column('asignaciones_materia', 'updated_at')
    op.drop_column('asignaciones_materia', 'created_at')
    op.drop_column('materias', 'updated_at')
    op.drop_column('materias', 'created_at')
    op.drop_column('docentes', 'updated_at')
    op.drop_column('docentes', 'created_at')
