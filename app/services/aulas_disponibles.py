from sqlalchemy.orm import Session
from datetime import time
from app.models.clase_programada import ClaseProgramada
from app.models.aula import Aula
from app.enums import DiaSemanaEnum


def obtener_aulas_disponibles(
    db: Session, dia: DiaSemanaEnum, hora_inicio: time, hora_fin: time
):
    clases = (
        db.query(ClaseProgramada)
        .filter(ClaseProgramada.dia == dia)
        .filter(ClaseProgramada.hora_inicio < hora_fin, ClaseProgramada.hora_fin > hora_inicio)
        .all()
    )

    aulas_ocupadas = {clase.aula_id for clase in clases}
    todas_las_aulas = db.query(Aula).all()

    return [aula for aula in todas_las_aulas if aula.id not in aulas_ocupadas]
