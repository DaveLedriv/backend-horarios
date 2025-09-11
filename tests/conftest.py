import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import Base
from app.models.facultad import Facultad
from app.models.plan_estudio import PlanEstudio
from app.models.docente import Docente
from app.models.materia import Materia


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def basic_data(session):
    facultad = Facultad(nombre="Ingeniería")
    plan = PlanEstudio(nombre="Plan 2024", facultad=facultad)
    docente1 = Docente(nombre="Docente Uno", correo="d1@example.com", numero_empleado="1", facultad=facultad)
    docente2 = Docente(nombre="Docente Dos", correo="d2@example.com", numero_empleado="2", facultad=facultad)
    materia = Materia(nombre="Mat", codigo="MAT1", creditos=3, plan_estudio=plan, permite_superposicion=False)
    materia_super = Materia(nombre="Mat Sup", codigo="MAT2", creditos=3, plan_estudio=plan, permite_superposicion=True)
    session.add_all([facultad, plan, docente1, docente2, materia, materia_super])
    session.commit()
    return {
        "docente1": docente1,
        "docente2": docente2,
        "materia": materia,
        "materia_super": materia_super,
    }
