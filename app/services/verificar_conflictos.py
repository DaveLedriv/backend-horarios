from sqlalchemy.orm import Session
from typing import Tuple

from app.models.clase_programada import ClaseProgramada
from app.models.materia import Materia
from app.models.disponibilidad_docente import DisponibilidadDocente

def verificar_conflictos(
    db: Session,
    docente_id: int,
    aula: str,
    dia: str,
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
        aula: Nombre del aula.
        dia: Día de la semana.
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
    if materia and materia.permite_superposicion:
        return False, True  # Se permite superposición, no hay conflicto y disponibilidad asumida

    # Verificar disponibilidad del docente
    disponible = db.query(DisponibilidadDocente).filter(
        DisponibilidadDocente.docente_id == docente_id,
        DisponibilidadDocente.dia == dia,
        DisponibilidadDocente.hora_inicio <= hora_inicio,
        DisponibilidadDocente.hora_fin >= hora_fin,
    ).first()
    docente_disponible = disponible is not None

    query = db.query(ClaseProgramada).filter(
        ClaseProgramada.dia == dia,
        ClaseProgramada.hora_inicio < hora_fin,
        ClaseProgramada.hora_fin > hora_inicio,
        (
            (ClaseProgramada.docente_id == docente_id) |
            (ClaseProgramada.aula == aula)
        )
    )

    if clase_id_ignorar:
        query = query.filter(ClaseProgramada.id != clase_id_ignorar)

    conflicto = db.query(query.exists()).scalar()
    return conflicto, docente_disponible
