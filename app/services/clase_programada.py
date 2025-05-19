# app/services/clase_programada.py

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.clase_programada import ClaseProgramada

def verificar_conflictos(
    db: Session,
    docente_id: int,
    aula: str,
    dia: str,
    hora_inicio,
    hora_fin,
    clase_id_ignorar=None
):
    conflicto = db.query(ClaseProgramada).filter(
        ClaseProgramada.dia == dia,
        or_(
            and_(
                ClaseProgramada.docente_id == docente_id,
                ClaseProgramada.hora_inicio < hora_fin,
                ClaseProgramada.hora_fin > hora_inicio
            ),
            and_(
                ClaseProgramada.aula == aula,
                ClaseProgramada.hora_inicio < hora_fin,
                ClaseProgramada.hora_fin > hora_inicio
            )
        )
    )

    if clase_id_ignorar:
        conflicto = conflicto.filter(ClaseProgramada.id != clase_id_ignorar)

    return conflicto.first() is not None
