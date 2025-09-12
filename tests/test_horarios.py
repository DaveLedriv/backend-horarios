import os
import sys
from datetime import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from app.core.database import Base, get_db
from app.models import (
    Facultad,
    PlanEstudio,
    Docente,
    Materia,
    Aula,
    ClaseProgramada,
    AsignacionMateria,
)
from app.enums import DiaSemanaEnum


@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def crear_datos_base(db):
    facultad = Facultad(nombre="Facultad X")
    db.add(facultad)
    db.commit()

    plan = PlanEstudio(nombre="Plan X", facultad_id=facultad.id)
    db.add(plan)
    db.commit()

    docente = Docente(
        nombre="Docente Uno",
        correo="docente@example.com",
        numero_empleado="EMP001",
        facultad_id=facultad.id,
    )
    aula = Aula(nombre="Aula 101", capacidad=30)
    materia = Materia(
        nombre="Materia X",
        codigo="MAT101",
        creditos=3,
        plan_estudio_id=plan.id,
    )
    db.add_all([docente, aula, materia])
    db.commit()

    asignacion = AsignacionMateria(docente_id=docente.id, materia_id=materia.id)
    db.add(asignacion)
    db.commit()

    clase = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula_id=aula.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    db.add(clase)
    db.commit()
    return docente.id, aula.id, clase.id, materia.id, asignacion.id


def test_horario_docente_devuelve_clases(client, session):
    docente_id, aula_id, clase_id, materia_id, asignacion_id = crear_datos_base(session)
    response = client.get(f"/horarios/docente/{docente_id}")
    assert response.status_code == 200
    data = response.json()
    assert "clases" in data
    assert len(data["clases"]) == 1
    clase = data["clases"][0]
    assert clase["id"] == clase_id
    assert clase["asignacion"]["id"] == asignacion_id
    assert clase["asignacion"]["docente"]["id"] == docente_id
    assert clase["aula"]["id"] == aula_id


def test_horario_aula_devuelve_clases(client, session):
    docente_id, aula_id, clase_id, materia_id, asignacion_id = crear_datos_base(session)
    response = client.get(f"/horarios/aula/{aula_id}")
    assert response.status_code == 200
    data = response.json()
    assert "clases" in data
    assert len(data["clases"]) == 1
    clase = data["clases"][0]
    assert clase["id"] == clase_id
    assert clase["asignacion"]["id"] == asignacion_id
    assert clase["aula"]["id"] == aula_id
