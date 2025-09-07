from sqlalchemy.orm import Session
from typing import Tuple

from app.models.clase_programada import ClaseProgramada
from app.models.materia import Materia


def verificar_conflictos(
    db: Session,
    docente_id: int,

    hora_inicio,
    hora_fin,
    materia_id: int,
    clase_id_ignorar: int = None,
) -> Tuple[bool, bool]:
    """
    Valida si hay empalmes de horario por docente o aula y
    verifica si el docente tiene disponibilidad en el horario propuesto,
    a menos que la materia permita superposición.

    Args:
        db: Sesión de base de datos.
        docente_id: ID del docente.

        hora_inicio: Hora de inicio de la clase.
        hora_fin: Hora de fin de la clase.
        materia_id: ID de la materia.
        clase_id_ignorar: ID de clase a ignorar (por ejemplo, durante edición).

    Returns:
        Una tupla con dos valores:
            - bool: True si hay conflicto con otra clase, False si no.
            - bool: True si el docente está disponible, False en caso contrario.
    """
    materia = db.query(Materia).filter(Materia.id == materia_id).first()


    query = db.query(ClaseProgramada).filter(
        ClaseProgramada.dia == dia,
        ClaseProgramada.hora_inicio < hora_fin,
        ClaseProgramada.hora_fin > hora_inicio,

    )

    if materia and materia.permite_superposicion:
        # Siempre validar conflicto por aula aunque se permita superposición
        query = query.filter(ClaseProgramada.aula == aula)
    else:
        # Si no se permite superposición, validar por docente o aula
        query = query.filter(
            (
                (ClaseProgramada.docente_id == docente_id) |
                (ClaseProgramada.aula == aula)
            )
        )

    if clase_id_ignorar:
        query = query.filter(ClaseProgramada.id != clase_id_ignorar)

    conflicto = db.query(query.exists()).scalar()
    return conflicto, docente_disponible
