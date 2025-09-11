import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from app.core.database import Base, get_db
from app.models import Facultad, Docente


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


def crear_docente(db):
    facultad = Facultad(nombre="Facultad X")
    db.add(facultad)
    db.commit()
    docente = Docente(
        nombre="Docente Uno",
        correo="docente@example.com",
        numero_empleado="EMP001",
        facultad_id=facultad.id,
    )
    db.add(docente)
    db.commit()
    return docente.id


def test_crear_disponibilidad_valida(client, session):
    docente_id = crear_docente(session)
    data = {
        "docente_id": docente_id,
        "disponibles": [
            {"dia": "lunes", "hora_inicio": "09:00", "hora_fin": "10:00"}
        ],
    }
    response = client.post("/disponibilidad/", json=data)
    assert response.status_code == 201
    assert response.json()["mensaje"] == "Disponibilidades registradas correctamente"


def test_crear_disponibilidad_traslapada(client, session):
    docente_id = crear_docente(session)

    data1 = {
        "docente_id": docente_id,
        "disponibles": [
            {"dia": "lunes", "hora_inicio": "09:00", "hora_fin": "10:00"}
        ],
    }
    response1 = client.post("/disponibilidad/", json=data1)
    assert response1.status_code == 201

    data2 = {
        "docente_id": docente_id,
        "disponibles": [
            {"dia": "lunes", "hora_inicio": "09:30", "hora_fin": "10:30"}
        ],
    }
    response2 = client.post("/disponibilidad/", json=data2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Bloques de disponibilidad traslapados"
