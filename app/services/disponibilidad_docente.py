from sqlalchemy.orm import Session
from app.models.clase_programada import ClaseProgramada
from app.models.clase_programada import DiaSemanaEnum
from datetime import time
from typing import List, Optional

# Rango horario base
HORARIO_INICIO = time(7, 0)
HORARIO_FIN = time(21, 0)

DIAS_SEMANA = [
    "lunes", "martes", "miércoles", "jueves", "viernes"
]

def obtener_disponibilidad_docente(
    db: Session,
    docente_id: int,
    dia: Optional[DiaSemanaEnum] = None,
    desde: Optional[time] = None,
    hasta: Optional[time] = None
) -> List[dict]:
    clases = db.query(ClaseProgramada).filter(
        ClaseProgramada.docente_id == docente_id
    ).all()

    disponibilidad = []

    dias_a_consultar = [dia] if dia else DIAS_SEMANA

    for dia_actual in dias_a_consultar:
        clases_dia = sorted(
            [c for c in clases if c.dia == dia_actual],
            key=lambda x: x.hora_inicio
        )

        inicio_dia = desde or HORARIO_INICIO
        fin_dia = hasta or HORARIO_FIN
        hora_actual = inicio_dia

        for clase in clases_dia:
            if clase.hora_inicio >= fin_dia:
                break
            if clase.hora_fin <= hora_actual:
                continue

            if clase.hora_inicio > hora_actual:
                disponibilidad.append({
                    "dia": dia_actual,
                    "hora_inicio": hora_actual,
                    "hora_fin": min(clase.hora_inicio, fin_dia)
                })

            hora_actual = max(hora_actual, clase.hora_fin)

        if hora_actual < fin_dia:
            disponibilidad.append({
                "dia": dia_actual,
                "hora_inicio": hora_actual,
                "hora_fin": fin_dia
            })

    return disponibilidad
