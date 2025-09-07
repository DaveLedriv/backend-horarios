from sqlalchemy.orm import Session
from app.models.clase_programada import ClaseProgramada
from datetime import time
from typing import List, Optional
from app.models.disponibilidad_docente import DisponibilidadDocente
from app.enums import DiaSemanaEnum


# Rango horario base
HORARIO_INICIO = time(7, 0)
HORARIO_FIN = time(21, 0)

DIAS_SEMANA = [
    DiaSemanaEnum.lunes,
    DiaSemanaEnum.martes,
    DiaSemanaEnum.miercoles,
    DiaSemanaEnum.jueves,
    DiaSemanaEnum.viernes,
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

def obtener_bloques_disponibles_registrados(
    db: Session,
    docente_id: int
) -> List[dict]:
    bloques = db.query(DisponibilidadDocente).filter(
        DisponibilidadDocente.docente_id == docente_id
    ).all()

    return [
        {
            "dia": b.dia,
            "hora_inicio": b.hora_inicio,
            "hora_fin": b.hora_fin
        }
        for b in bloques
    ]


def obtener_disponibilidad_docente_completa(
    db: Session,
    docente_id: int,
    dia: Optional[DiaSemanaEnum] = None,
    desde: Optional[time] = None,
    hasta: Optional[time] = None,
) -> dict:
    """
    Combina la disponibilidad registrada con los tiempos libres calculados.

    La disponibilidad registrada corresponde a los bloques que el docente ha
    definido explícitamente como disponibles. Los tiempos libres calculados se
    derivan del horario de clases programadas y representan las horas sin
    clases dentro del rango consultado.
    """

    registrada = obtener_bloques_disponibles_registrados(db, docente_id)

    # Filtrar la disponibilidad registrada según los parámetros recibidos
    if dia or desde or hasta:
        filtrada = []
        for bloque in registrada:
            if dia and bloque["dia"] != dia:
                continue

            inicio = bloque["hora_inicio"]
            fin = bloque["hora_fin"]

            if desde and fin <= desde:
                continue
            if hasta and inicio >= hasta:
                continue

            if desde:
                inicio = max(inicio, desde)
            if hasta:
                fin = min(fin, hasta)

            filtrada.append({
                "dia": bloque["dia"],
                "hora_inicio": inicio,
                "hora_fin": fin,
            })

        registrada = filtrada

    tiempos_libres = obtener_disponibilidad_docente(
        db, docente_id, dia, desde, hasta
    )

    return {
        "registrada": registrada,
        "tiempos_libres": tiempos_libres,
    }
