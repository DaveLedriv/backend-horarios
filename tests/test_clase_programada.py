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
    Grupo,
    DisponibilidadDocente,
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
    grupo = Grupo(nombre="Grupo A", plan_estudio_id=plan.id, num_estudiantes=25)
    db.add_all([docente, aula, materia, grupo])
    db.commit()

    asignacion = AsignacionMateria(docente_id=docente.id, materia_id=materia.id)
    db.add(asignacion)
    db.commit()

    clase = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula_id=aula.id,
        grupo_id=grupo.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    db.add(clase)
    db.commit()
    return docente.id, aula.id, clase.id, materia.id, asignacion.id, grupo.id


def test_crear_clase_programada_sobrecupo(client, session):
    facultad = Facultad(nombre="Facultad Y")
    session.add(facultad)
    session.commit()

    plan = PlanEstudio(nombre="Plan Y", facultad_id=facultad.id)
    session.add(plan)
    session.commit()

    docente = Docente(
        nombre="Docente Dos",
        correo="docente2@example.com",
        numero_empleado="EMP002",
        facultad_id=facultad.id,
    )
    session.add(docente)
    session.commit()

    aula = Aula(nombre="Aula 201", capacidad=30)
    materia = Materia(
        nombre="Materia Y",
        codigo="MAT201",
        creditos=4,
        plan_estudio_id=plan.id,
    )
    grupo = Grupo(nombre="Grupo B", plan_estudio_id=plan.id, num_estudiantes=35)
    session.add_all([aula, materia, grupo])
    session.commit()

    asignacion = AsignacionMateria(docente_id=docente.id, materia_id=materia.id)
    session.add(asignacion)
    session.commit()

    disponibilidad = DisponibilidadDocente(
        docente_id=docente.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )
    session.add(disponibilidad)
    session.commit()

    data = {
        "docente_id": docente.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "lunes",
        "hora_inicio": "09:00 AM",
        "hora_fin": "10:00 AM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "El grupo excede la capacidad del aula."


def test_obtener_clase_programada(client, session):
    (
        docente_id,
        aula_id,
        clase_id,
        materia_id,
        asignacion_id,
        grupo_id,
    ) = crear_datos_base(session)
    response = client.get(f"/clases-programadas/{clase_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == clase_id
    assert data["docente_id"] == docente_id
    assert data["materia_id"] == materia_id
    assert data["aula_id"] == aula_id
    assert data["dia"] == "lunes"
    assert data["hora_inicio"] == "09:00:00"
    assert data["hora_fin"] == "10:00:00"
    assert data["asignacion"]["id"] == asignacion_id
    assert data["asignacion"]["docente"]["id"] == docente_id
    assert data["asignacion"]["materia"]["id"] == materia_id
    assert data["aula"]["id"] == aula_id
    assert data["grupo"]["id"] == grupo_id


def test_no_permite_superposicion_mismo_grupo(client, session):
    facultad = Facultad(nombre="Facultad Z")
    session.add(facultad)
    session.commit()

    plan = PlanEstudio(nombre="Plan Z", facultad_id=facultad.id)
    session.add(plan)
    session.commit()

    docente_uno = Docente(
        nombre="Docente Tres",
        correo="docente3@example.com",
        numero_empleado="EMP003",
        facultad_id=facultad.id,
    )
    docente_dos = Docente(
        nombre="Docente Cuatro",
        correo="docente4@example.com",
        numero_empleado="EMP004",
        facultad_id=facultad.id,
    )
    session.add_all([docente_uno, docente_dos])
    session.commit()

    aula_uno = Aula(nombre="Aula 301", capacidad=30)
    aula_dos = Aula(nombre="Aula 302", capacidad=30)
    materia = Materia(
        nombre="Materia Z",
        codigo="MAT301",
        creditos=3,
        plan_estudio_id=plan.id,
    )
    grupo = Grupo(nombre="Grupo C", plan_estudio_id=plan.id, num_estudiantes=20)
    session.add_all([aula_uno, aula_dos, materia, grupo])
    session.commit()

    asignacion_uno = AsignacionMateria(
        docente_id=docente_uno.id, materia_id=materia.id
    )
    asignacion_dos = AsignacionMateria(
        docente_id=docente_dos.id, materia_id=materia.id
    )
    session.add_all([asignacion_uno, asignacion_dos])
    session.commit()

    disponibilidad_uno = DisponibilidadDocente(
        docente_id=docente_uno.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )
    disponibilidad_dos = DisponibilidadDocente(
        docente_id=docente_dos.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )
    session.add_all([disponibilidad_uno, disponibilidad_dos])
    session.commit()

    primera_clase = {
        "docente_id": docente_uno.id,
        "materia_id": materia.id,
        "aula_id": aula_uno.id,
        "grupo_id": grupo.id,
        "dia": "lunes",
        "hora_inicio": "09:00 AM",
        "hora_fin": "10:00 AM",
    }

    respuesta_primera = client.post("/clases-programadas", json=primera_clase)
    assert respuesta_primera.status_code == 200

    segunda_clase = {
        "docente_id": docente_dos.id,
        "materia_id": materia.id,
        "aula_id": aula_dos.id,
        "grupo_id": grupo.id,
        "dia": "lunes",
        "hora_inicio": "09:30 AM",
        "hora_fin": "10:30 AM",
    }

    respuesta_segunda = client.post("/clases-programadas", json=segunda_clase)

    assert respuesta_segunda.status_code == 400
    assert "Conflicto" in respuesta_segunda.json()["detail"]
