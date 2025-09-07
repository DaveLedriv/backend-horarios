from sqlalchemy.orm import Session
from app.models.clase_programada import ClaseProgramada
from app.models.materia import Materia


def verificar_conflictos(
    db: Session,
    docente_id: int,
    aula: str,
    dia: str,
    hora_inicio,
    hora_fin,
    materia_id: int,
    clase_id_ignorar: int = None,
) -> bool:
    """
    Valida si hay empalmes de horario por docente o aula,
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
        True si hay conflicto, False si no.
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

    return db.query(query.exists()).scalar()
