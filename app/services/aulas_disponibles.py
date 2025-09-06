from sqlalchemy.orm import Session
from datetime import time
from app.models.clase_programada import ClaseProgramada
from app.enums import DiaSemanaEnum


def obtener_aulas_disponibles(
    db: Session, dia: DiaSemanaEnum, hora_inicio: time, hora_fin: time
):
    clases = db.query(ClaseProgramada).filter(ClaseProgramada.dia == dia).all()

    aulas_ocupadas = {
        clase.aula
        for clase in clases
        if clase.hora_inicio < hora_fin and clase.hora_fin > hora_inicio
    }

    # Obtener todas las aulas registradas
    todas_las_aulas = db.query(ClaseProgramada.aula).distinct().all()
    aulas_todas = {aula[0] for aula in todas_las_aulas}

    return list(aulas_todas - aulas_ocupadas)
