from datetime import time

from app.enums import DiaSemanaEnum
from app.models.clase_programada import ClaseProgramada
from app.services.verificar_conflictos import verificar_conflictos


def test_conflicto_por_docente(session, basic_data):
    docente = basic_data["docente1"]
    materia = basic_data["materia"]
    clase = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    session.add(clase)
    session.commit()

    conflicto = verificar_conflictos(
        db=session,
        docente_id=docente.id,
        aula="A2",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 30),
        hora_fin=time(10, 30),
        materia_id=materia.id,
    )
    assert conflicto is True


def test_conflicto_por_aula(session, basic_data):
    docente1 = basic_data["docente1"]
    docente2 = basic_data["docente2"]
    materia = basic_data["materia"]
    clase = ClaseProgramada(
        docente_id=docente1.id,
        materia_id=materia.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    session.add(clase)
    session.commit()

    conflicto = verificar_conflictos(
        db=session,
        docente_id=docente2.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 30),
        hora_fin=time(10, 30),
        materia_id=materia.id,
    )
    assert conflicto is True


def test_superposicion_permitida(session, basic_data):
    docente = basic_data["docente1"]
    materia = basic_data["materia"]
    materia_super = basic_data["materia_super"]
    clase = ClaseProgramada(
        docente_id=docente.id,
        materia_id=materia.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
    )
    session.add(clase)
    session.commit()

    conflicto = verificar_conflictos(
        db=session,
        docente_id=docente.id,
        aula="A1",
        dia=DiaSemanaEnum.lunes,
        hora_inicio=time(9, 30),
        hora_fin=time(10, 30),
        materia_id=materia_super.id,
    )
    assert conflicto is False
