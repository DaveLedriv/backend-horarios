from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Tuple

from app.enums import DiaSemanaEnum
from app.models.clase_programada import ClaseProgramada
from app.models.disponibilidad_docente import DisponibilidadDocente
from app.models.materia import Materia


def verificar_conflictos(
    db: Session,
    docente_id: int,
    dia: DiaSemanaEnum,
    hora_inicio,
    hora_fin,
    materia_id: int,
    aula_id: int,
    grupo_id: int,
    clase_id_ignorar: int = None,
) -> Tuple[bool, bool]:
    """Valida conflictos y disponibilidad de un docente.

    Comprueba si existe conflicto de horario por docente o aula y verifica
    que el bloque solicitado esté dentro de la disponibilidad registrada del
    docente. Si la materia permite superposición solo se valida el conflicto
    por aula.

    Args:
        db: Sesión de base de datos.
        docente_id: ID del docente.
        dia: Día de la semana de la clase.
        hora_inicio: Hora de inicio de la clase.
        hora_fin: Hora de fin de la clase.
        materia_id: ID de la materia.
        aula_id: ID del aula.
        grupo_id: ID del grupo.
        clase_id_ignorar: ID de clase a ignorar (por ejemplo, durante edición).

    Returns:
        Tuple[bool, bool]:
            - Primer valor indica si existe conflicto.
            - Segundo valor indica si el docente está disponible.
    """

    materia = db.query(Materia).filter(Materia.id == materia_id).first()

    query = db.query(ClaseProgramada).filter(
        ClaseProgramada.dia == dia,
        ClaseProgramada.hora_inicio < hora_fin,
        ClaseProgramada.hora_fin > hora_inicio,
    )

    if clase_id_ignorar:
        query = query.filter(ClaseProgramada.id != clase_id_ignorar)

    condiciones_conflicto = [ClaseProgramada.grupo_id == grupo_id]

    if materia and materia.permite_superposicion:
        # Siempre validar conflicto por aula aunque se permita superposición
        condiciones_conflicto.append(ClaseProgramada.aula_id == aula_id)
    else:
        # Si no se permite superposición, validar por docente o aula
        condiciones_conflicto.extend(
            [
                ClaseProgramada.docente_id == docente_id,
                ClaseProgramada.aula_id == aula_id,
            ]
        )

    query = query.filter(or_(*condiciones_conflicto))

    conflicto = db.query(query.exists()).scalar()

    disponibilidad = db.query(DisponibilidadDocente).filter(
        DisponibilidadDocente.docente_id == docente_id,
        DisponibilidadDocente.dia == dia,
        DisponibilidadDocente.hora_inicio <= hora_inicio,
        DisponibilidadDocente.hora_fin >= hora_fin,
    ).first()

    docente_disponible = disponibilidad is not None

    return conflicto, docente_disponible
