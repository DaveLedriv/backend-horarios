from datetime import time

from app.enums import DiaSemanaEnum
from app.models.clase_programada import ClaseProgramada
from app.schemas.disponibilidad_docente import BloqueDisponible, DisponibilidadDocenteMultipleCreate
from app.routers.disponibilidad import crear_disponibilidad
from app.services.disponibilidad_docente import obtener_disponibilidad_docente, obtener_bloques_disponibles_registrados


def test_obtener_disponibilidad_docente(session, basic_data):
    docente = basic_data["docente1"]
    materia = basic_data["materia"]
    clase1 = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    clase2 = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(11, 0),
        hora_fin=time(12, 0),
    )
    session.add_all([clase1, clase2])
    session.commit()

    bloques = obtener_disponibilidad_docente(
        db=session,
        docente_id=docente.id,
        dia=DiaSemanaEnum.lunes,
        desde=time(8, 0),
        hasta=time(12, 0),
    )
    assert bloques == [
        {"dia": DiaSemanaEnum.lunes, "hora_inicio": time(8, 0), "hora_fin": time(9, 0)},
        {"dia": DiaSemanaEnum.lunes, "hora_inicio": time(10, 0), "hora_fin": time(11, 0)},
    ]


def test_insercion_disponibilidad(session, basic_data):
    docente = basic_data["docente1"]
    payload = DisponibilidadDocenteMultipleCreate(
        docente_id=docente.id,
        disponibles=[
            BloqueDisponible(dia=DiaSemanaEnum.lunes, hora_inicio=time(8, 0), hora_fin=time(9, 0)),
            BloqueDisponible(dia=DiaSemanaEnum.martes, hora_inicio=time(10, 0), hora_fin=time(11, 0)),
        ],
    )

    crear_disponibilidad(payload, db=session)

    bloques = obtener_bloques_disponibles_registrados(session, docente.id)
    assert len(bloques) == 2
    assert bloques[0]["dia"] == DiaSemanaEnum.lunes
    assert bloques[1]["dia"] == DiaSemanaEnum.martes
