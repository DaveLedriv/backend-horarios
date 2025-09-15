from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.enums import DiaSemanaEnum
from app.models.clase_programada import ClaseProgramada

_REFERENCE_DATE = date(1900, 1, 1)


def _calcular_duracion_en_horas(hora_inicio: time, hora_fin: time) -> float:
    """Retorna la duración entre dos horas expresada en horas decimales."""

    inicio = datetime.combine(_REFERENCE_DATE, hora_inicio)
    fin = datetime.combine(_REFERENCE_DATE, hora_fin)
    return (fin - inicio).total_seconds() / 3600


def _unir_intervalos(bloques: List[Tuple[time, time]]) -> List[Tuple[time, time]]:
    """Une intervalos continuos u overlapeados y devuelve bloques ordenados."""

    if not bloques:
        return []

    bloques_ordenados = sorted(bloques, key=lambda bloque: bloque[0])
    bloques_unidos: List[Tuple[time, time]] = [bloques_ordenados[0]]

    for inicio, fin in bloques_ordenados[1:]:
        ultimo_inicio, ultimo_fin = bloques_unidos[-1]
        if inicio <= ultimo_fin:
            bloques_unidos[-1] = (ultimo_inicio, max(ultimo_fin, fin))
        else:
            bloques_unidos.append((inicio, fin))

    return bloques_unidos


def _obtener_clases(
    db: Session,
    campo_relacion,
    entidad_id: int,
    dia: Optional[DiaSemanaEnum] = None,
    clase_id_ignorar: Optional[int] = None,
) -> List[ClaseProgramada]:
    """Obtiene las clases filtradas por docente o grupo."""

    query = db.query(ClaseProgramada).filter(campo_relacion == entidad_id)

    if dia is not None:
        query = query.filter(ClaseProgramada.dia == dia)

    if clase_id_ignorar is not None:
        query = query.filter(ClaseProgramada.id != clase_id_ignorar)

    return query.all()


def _obtener_horas_continuas(
    db: Session,
    campo_relacion,
    entidad_id: int,
    dia: DiaSemanaEnum,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    bloques_existentes = [
        (clase.hora_inicio, clase.hora_fin)
        for clase in _obtener_clases(db, campo_relacion, entidad_id, dia, clase_id_ignorar)
    ]

    bloques_existentes.append((hora_inicio, hora_fin))
    bloques_unidos = _unir_intervalos(bloques_existentes)
    return max(_calcular_duracion_en_horas(inicio, fin) for inicio, fin in bloques_unidos)


def _obtener_total_horas(
    db: Session,
    campo_relacion,
    entidad_id: int,
    hora_inicio: time,
    hora_fin: time,
    dia: Optional[DiaSemanaEnum] = None,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    clases = _obtener_clases(db, campo_relacion, entidad_id, dia, clase_id_ignorar)
    total = sum(_calcular_duracion_en_horas(c.hora_inicio, c.hora_fin) for c in clases)
    return total + _calcular_duracion_en_horas(hora_inicio, hora_fin)


def obtener_horas_continuas_docente(
    db: Session,
    docente_id: int,
    dia: DiaSemanaEnum,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Calcula las horas continuas máximas de un docente en un día."""

    return _obtener_horas_continuas(
        db,
        ClaseProgramada.docente_id,
        docente_id,
        dia,
        hora_inicio,
        hora_fin,
        clase_id_ignorar,
    )


def obtener_total_horas_diarias_docente(
    db: Session,
    docente_id: int,
    dia: DiaSemanaEnum,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Devuelve la carga diaria total de un docente incluyendo una nueva clase."""

    return _obtener_total_horas(
        db,
        ClaseProgramada.docente_id,
        docente_id,
        hora_inicio,
        hora_fin,
        dia,
        clase_id_ignorar,
    )


def obtener_total_horas_semanales_docente(
    db: Session,
    docente_id: int,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Devuelve la carga semanal total de un docente incluyendo una nueva clase."""

    return _obtener_total_horas(
        db,
        ClaseProgramada.docente_id,
        docente_id,
        hora_inicio,
        hora_fin,
        clase_id_ignorar=clase_id_ignorar,
    )


def obtener_horas_continuas_grupo(
    db: Session,
    grupo_id: int,
    dia: DiaSemanaEnum,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Calcula las horas continuas máximas de un grupo en un día."""

    return _obtener_horas_continuas(
        db,
        ClaseProgramada.grupo_id,
        grupo_id,
        dia,
        hora_inicio,
        hora_fin,
        clase_id_ignorar,
    )


def obtener_total_horas_diarias_grupo(
    db: Session,
    grupo_id: int,
    dia: DiaSemanaEnum,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Devuelve la carga diaria total de un grupo incluyendo una nueva clase."""

    return _obtener_total_horas(
        db,
        ClaseProgramada.grupo_id,
        grupo_id,
        hora_inicio,
        hora_fin,
        dia,
        clase_id_ignorar,
    )


def obtener_total_horas_semanales_grupo(
    db: Session,
    grupo_id: int,
    hora_inicio: time,
    hora_fin: time,
    clase_id_ignorar: Optional[int] = None,
) -> float:
    """Devuelve la carga semanal total de un grupo incluyendo una nueva clase."""

    return _obtener_total_horas(
        db,
        ClaseProgramada.grupo_id,
        grupo_id,
        hora_inicio,
        hora_fin,
        clase_id_ignorar=clase_id_ignorar,
    )
