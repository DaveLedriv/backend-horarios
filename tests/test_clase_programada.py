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


def crear_base_academica(db, sufijo: str):
    facultad = Facultad(nombre=f"Facultad {sufijo}")
    db.add(facultad)
    db.commit()

    plan = PlanEstudio(nombre=f"Plan {sufijo}", facultad_id=facultad.id)
    db.add(plan)
    db.commit()

    materia = Materia(
        nombre=f"Materia {sufijo}",
        codigo=f"MAT_{sufijo}",
        creditos=4,
        plan_estudio_id=plan.id,
    )
    aula = Aula(nombre=f"Aula {sufijo}", capacidad=40)
    grupo = Grupo(nombre=f"Grupo {sufijo}", plan_estudio_id=plan.id, num_estudiantes=30)
    db.add_all([materia, aula, grupo])
    db.commit()

    return facultad, plan, materia, aula, grupo


def crear_docente_con_disponibilidad(
    db,
    facultad_id: int,
    nombre: str,
    correo: str,
    numero_empleado: str,
    disponibilidad,
):
    docente = Docente(
        nombre=nombre,
        correo=correo,
        numero_empleado=numero_empleado,
        facultad_id=facultad_id,
    )
    db.add(docente)
    db.commit()

    registros_disponibilidad = [
        DisponibilidadDocente(
            docente_id=docente.id,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
        )
        for dia, hora_inicio, hora_fin in disponibilidad
    ]
    db.add_all(registros_disponibilidad)
    db.commit()

    return docente


def asignar_docente_a_materia(db, docente_id: int, materia_id: int):
    asignacion = AsignacionMateria(docente_id=docente_id, materia_id=materia_id)
    db.add(asignacion)
    db.commit()
    return asignacion


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


def test_crear_clase_programada_excede_horas_continuas_docente(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "DOC_CONT")
    docente = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Continuo",
        "docente.continuo@example.com",
        "EMP100",
        [(DiaSemanaEnum.lunes, time(8, 0), time(14, 0))],
    )
    asignar_docente_a_materia(session, docente.id, materia.id)

    clase_existente = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula_id=aula.id,
        grupo_id=grupo.id,
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(8, 0),
        hora_fin=time(12, 0),
    )
    session.add(clase_existente)
    session.commit()

    data = {
        "docente_id": docente.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "lunes",
        "hora_inicio": "12:00 PM",
        "hora_fin": "02:00 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "El docente excede las horas continuas permitidas."
    )


def test_crear_clase_programada_excede_horas_diarias_docente(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "DOC_DAY")
    docente = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Diario",
        "docente.diario@example.com",
        "EMP101",
        [(DiaSemanaEnum.martes, time(8, 0), time(19, 0))],
    )
    asignar_docente_a_materia(session, docente.id, materia.id)

    clases_existentes = [
        ClaseProgramada(
            docente_id=docente.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.martes,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
        ),
        ClaseProgramada(
            docente_id=docente.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.martes,
            hora_inicio=time(10, 30),
            hora_fin=time(13, 30),
        ),
    ]
    session.add_all(clases_existentes)
    session.commit()

    data = {
        "docente_id": docente.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "martes",
        "hora_inicio": "02:00 PM",
        "hora_fin": "06:00 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "El docente excede las horas diarias permitidas."


def test_crear_clase_programada_excede_horas_semanales_docente(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "DOC_WEEK")
    docente = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Semanal",
        "docente.semanal@example.com",
        "EMP102",
        [
            (DiaSemanaEnum.lunes, time(8, 0), time(13, 0)),
            (DiaSemanaEnum.martes, time(8, 0), time(13, 0)),
            (DiaSemanaEnum.miercoles, time(8, 0), time(13, 0)),
            (DiaSemanaEnum.jueves, time(8, 0), time(13, 0)),
        ],
    )
    asignar_docente_a_materia(session, docente.id, materia.id)

    for dia in [
        DiaSemanaEnum.lunes,
        DiaSemanaEnum.martes,
        DiaSemanaEnum.miercoles,
    ]:
        session.add(
            ClaseProgramada(
                docente_id=docente.id,
                materia_id=materia.id,
                aula_id=aula.id,
                grupo_id=grupo.id,
                dia=dia,
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0),
            )
        )
    session.commit()

    data = {
        "docente_id": docente.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "jueves",
        "hora_inicio": "08:00 AM",
        "hora_fin": "12:00 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "El docente excede las horas semanales permitidas."
    )


def test_crear_clase_programada_excede_horas_continuas_grupo(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "GRP_CONT")

    docente_uno = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Uno",
        "docente.grupo1@example.com",
        "EMP200",
        [(DiaSemanaEnum.lunes, time(8, 0), time(12, 0))],
    )
    docente_dos = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Dos",
        "docente.grupo2@example.com",
        "EMP201",
        [(DiaSemanaEnum.lunes, time(12, 0), time(16, 0))],
    )
    asignar_docente_a_materia(session, docente_uno.id, materia.id)
    asignar_docente_a_materia(session, docente_dos.id, materia.id)

    session.add(
        ClaseProgramada(
            docente_id=docente_uno.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.lunes,
            hora_inicio=time(8, 0),
            hora_fin=time(12, 0),
        )
    )
    session.commit()

    data = {
        "docente_id": docente_dos.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "lunes",
        "hora_inicio": "12:00 PM",
        "hora_fin": "04:00 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "El grupo excede las horas continuas permitidas."
    )


def test_crear_clase_programada_excede_horas_diarias_grupo(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "GRP_DAY")

    docente_uno = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Tres",
        "docente.grupo3@example.com",
        "EMP202",
        [(DiaSemanaEnum.miercoles, time(8, 0), time(10, 0))],
    )
    docente_dos = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Cuatro",
        "docente.grupo4@example.com",
        "EMP203",
        [(DiaSemanaEnum.miercoles, time(10, 30), time(13, 30))],
    )
    docente_tres = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Cinco",
        "docente.grupo5@example.com",
        "EMP204",
        [(DiaSemanaEnum.miercoles, time(14, 0), time(16, 0))],
    )
    docente_cuatro = crear_docente_con_disponibilidad(
        session,
        facultad.id,
        "Docente Grupo Seis",
        "docente.grupo6@example.com",
        "EMP205",
        [(DiaSemanaEnum.miercoles, time(16, 30), time(20, 0))],
    )

    for docente in [docente_uno, docente_dos, docente_tres, docente_cuatro]:
        asignar_docente_a_materia(session, docente.id, materia.id)

    clases_existentes = [
        ClaseProgramada(
            docente_id=docente_uno.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.miercoles,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
        ),
        ClaseProgramada(
            docente_id=docente_dos.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.miercoles,
            hora_inicio=time(10, 30),
            hora_fin=time(13, 30),
        ),
        ClaseProgramada(
            docente_id=docente_tres.id,
            materia_id=materia.id,
            aula_id=aula.id,
            grupo_id=grupo.id,
            dia=DiaSemanaEnum.miercoles,
            hora_inicio=time(14, 0),
            hora_fin=time(16, 0),
        ),
    ]
    session.add_all(clases_existentes)
    session.commit()

    data = {
        "docente_id": docente_cuatro.id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "miercoles",
        "hora_inicio": "04:30 PM",
        "hora_fin": "07:30 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "El grupo excede las horas diarias permitidas."


def test_crear_clase_programada_excede_horas_semanales_grupo(client, session):
    facultad, _, materia, aula, grupo = crear_base_academica(session, "GRP_WEEK")

    docentes = [
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Siete",
            "docente.grupo7@example.com",
            "EMP206",
            [(DiaSemanaEnum.lunes, time(8, 0), time(12, 0))],
        ),
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Ocho",
            "docente.grupo8@example.com",
            "EMP207",
            [(DiaSemanaEnum.martes, time(8, 0), time(12, 0))],
        ),
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Nueve",
            "docente.grupo9@example.com",
            "EMP208",
            [(DiaSemanaEnum.miercoles, time(8, 0), time(12, 0))],
        ),
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Diez",
            "docente.grupo10@example.com",
            "EMP209",
            [(DiaSemanaEnum.jueves, time(8, 0), time(12, 0))],
        ),
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Once",
            "docente.grupo11@example.com",
            "EMP210",
            [(DiaSemanaEnum.jueves, time(13, 0), time(15, 0))],
        ),
        crear_docente_con_disponibilidad(
            session,
            facultad.id,
            "Docente Grupo Doce",
            "docente.grupo12@example.com",
            "EMP211",
            [(DiaSemanaEnum.viernes, time(8, 0), time(12, 0))],
        ),
    ]

    for docente in docentes:
        asignar_docente_a_materia(session, docente.id, materia.id)

    clases_existentes = [
        (docentes[0], DiaSemanaEnum.lunes, time(8, 0), time(12, 0)),
        (docentes[1], DiaSemanaEnum.martes, time(8, 0), time(12, 0)),
        (docentes[2], DiaSemanaEnum.miercoles, time(8, 0), time(12, 0)),
        (docentes[3], DiaSemanaEnum.jueves, time(8, 0), time(12, 0)),
        (docentes[4], DiaSemanaEnum.jueves, time(13, 0), time(15, 0)),
    ]

    for docente, dia, hora_inicio, hora_fin in clases_existentes:
        session.add(
            ClaseProgramada(
                docente_id=docente.id,
                materia_id=materia.id,
                aula_id=aula.id,
                grupo_id=grupo.id,
                dia=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
            )
        )
    session.commit()

    data = {
        "docente_id": docentes[5].id,
        "materia_id": materia.id,
        "aula_id": aula.id,
        "grupo_id": grupo.id,
        "dia": "viernes",
        "hora_inicio": "08:00 AM",
        "hora_fin": "12:00 PM",
    }

    response = client.post("/clases-programadas", json=data)

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "El grupo excede las horas semanales permitidas."
    )
