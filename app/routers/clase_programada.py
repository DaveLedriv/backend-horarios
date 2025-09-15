from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, selectinload
from typing import List
from datetime import time

from app.enums import DiaSemanaEnum
from app.core.config import settings
from app.services.aulas_disponibles import obtener_aulas_disponibles
from app.schemas.clase_programada import (
    ClaseProgramadaCreate,
    ClaseProgramadaUpdate,
    ClaseProgramadaResponse,
    ClaseProgramadaDetalle,
)
from app.schemas.aula import AulaResponse
from app.models.clase_programada import ClaseProgramada
from app.models.asignacion_materia import AsignacionMateria
from app.models.grupo import Grupo
from app.models.aula import Aula
from app.core.database import get_db
from app.services import verificar_conflictos
from app.services.carga_academica import (
    obtener_horas_continuas_docente,
    obtener_horas_continuas_grupo,
    obtener_total_horas_diarias_docente,
    obtener_total_horas_diarias_grupo,
    obtener_total_horas_semanales_docente,
    obtener_total_horas_semanales_grupo,
)

router = APIRouter(prefix="/clases-programadas", tags=["Clases Programadas"])


@router.get("/", response_model=List[ClaseProgramadaResponse])
def listar_clases_programadas(db: Session = Depends(get_db)):
    return db.query(ClaseProgramada).all()


@router.get("/{clase_id}", response_model=ClaseProgramadaDetalle)
def obtener_clase_programada(clase_id: int, db: Session = Depends(get_db)):
    clase = (
        db.query(ClaseProgramada)
        .options(
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.docente),
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.materia),
            selectinload(ClaseProgramada.aula),
            selectinload(ClaseProgramada.grupo),
        )
        .filter(ClaseProgramada.id == clase_id)
        .first()
    )
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return clase


@router.post("", response_model=ClaseProgramadaResponse)
def crear_clase_programada(clase: ClaseProgramadaCreate, db: Session = Depends(get_db)):
    grupo = db.query(Grupo).filter(Grupo.id == clase.grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    aula = db.query(Aula).filter(Aula.id == clase.aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    if aula.capacidad is not None and grupo.num_estudiantes > aula.capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede la capacidad del aula.",
        )

    asignacion = db.query(AsignacionMateria).filter(
        AsignacionMateria.docente_id == clase.docente_id,
        AsignacionMateria.materia_id == clase.materia_id,
    ).first()
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Docente no asignado a la materia",
        )

    conflicto, disponible = verificar_conflictos(
        db=db,
        docente_id=clase.docente_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
        materia_id=clase.materia_id,
        aula_id=clase.aula_id,
        grupo_id=clase.grupo_id,
    )

    if not disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente no está disponible en ese horario.",
        )

    if conflicto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflicto detectado con otra clase en horario o aula.",
        )

    horas_continuas_docente = obtener_horas_continuas_docente(
        db=db,
        docente_id=clase.docente_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_continuas_docente > settings.MAX_HORAS_CONTINUAS_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas continuas permitidas.",
        )

    horas_diarias_docente = obtener_total_horas_diarias_docente(
        db=db,
        docente_id=clase.docente_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_diarias_docente > settings.MAX_HORAS_DIARIAS_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas diarias permitidas.",
        )

    horas_semanales_docente = obtener_total_horas_semanales_docente(
        db=db,
        docente_id=clase.docente_id,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_semanales_docente > settings.MAX_HORAS_SEMANALES_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas semanales permitidas.",
        )

    horas_continuas_grupo = obtener_horas_continuas_grupo(
        db=db,
        grupo_id=clase.grupo_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_continuas_grupo > settings.MAX_HORAS_CONTINUAS_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas continuas permitidas.",
        )

    horas_diarias_grupo = obtener_total_horas_diarias_grupo(
        db=db,
        grupo_id=clase.grupo_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_diarias_grupo > settings.MAX_HORAS_DIARIAS_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas diarias permitidas.",
        )

    horas_semanales_grupo = obtener_total_horas_semanales_grupo(
        db=db,
        grupo_id=clase.grupo_id,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
    )
    if horas_semanales_grupo > settings.MAX_HORAS_SEMANALES_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas semanales permitidas.",
        )

    nueva_clase = ClaseProgramada(**clase.dict())
    db.add(nueva_clase)
    db.commit()
    db.refresh(nueva_clase)
    return nueva_clase


@router.put("/{clase_id}", response_model=ClaseProgramadaResponse)
def actualizar_clase_programada(
    clase_id: int,
    clase_actualizada: ClaseProgramadaUpdate,
    db: Session = Depends(get_db),
):
    clase = db.query(ClaseProgramada).filter(ClaseProgramada.id == clase_id).first()

    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    grupo = db.query(Grupo).filter(Grupo.id == clase_actualizada.grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    aula = db.query(Aula).filter(Aula.id == clase_actualizada.aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    if aula.capacidad is not None and grupo.num_estudiantes > aula.capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede la capacidad del aula.",
        )

    asignacion = db.query(AsignacionMateria).filter(
        AsignacionMateria.docente_id == clase_actualizada.docente_id,
        AsignacionMateria.materia_id == clase_actualizada.materia_id,
    ).first()
    if not asignacion:
        raise HTTPException(
            status_code=400, detail="Docente no asignado a la materia"
        )

    conflicto, disponible = verificar_conflictos(
        db=db,
        docente_id=clase_actualizada.docente_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        materia_id=clase_actualizada.materia_id,
        aula_id=clase_actualizada.aula_id,
        grupo_id=clase_actualizada.grupo_id,
        clase_id_ignorar=clase_id,
    )

    if not disponible:
        raise HTTPException(
            status_code=400, detail="El docente no está disponible en ese horario."
        )

    if conflicto:
        raise HTTPException(
            status_code=400, detail="Conflicto detectado con otra clase"
        )

    horas_continuas_docente = obtener_horas_continuas_docente(
        db=db,
        docente_id=clase_actualizada.docente_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_continuas_docente > settings.MAX_HORAS_CONTINUAS_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas continuas permitidas.",
        )

    horas_diarias_docente = obtener_total_horas_diarias_docente(
        db=db,
        docente_id=clase_actualizada.docente_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_diarias_docente > settings.MAX_HORAS_DIARIAS_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas diarias permitidas.",
        )

    horas_semanales_docente = obtener_total_horas_semanales_docente(
        db=db,
        docente_id=clase_actualizada.docente_id,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_semanales_docente > settings.MAX_HORAS_SEMANALES_DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El docente excede las horas semanales permitidas.",
        )

    horas_continuas_grupo = obtener_horas_continuas_grupo(
        db=db,
        grupo_id=clase_actualizada.grupo_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_continuas_grupo > settings.MAX_HORAS_CONTINUAS_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas continuas permitidas.",
        )

    horas_diarias_grupo = obtener_total_horas_diarias_grupo(
        db=db,
        grupo_id=clase_actualizada.grupo_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_diarias_grupo > settings.MAX_HORAS_DIARIAS_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas diarias permitidas.",
        )

    horas_semanales_grupo = obtener_total_horas_semanales_grupo(
        db=db,
        grupo_id=clase_actualizada.grupo_id,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        clase_id_ignorar=clase_id,
    )
    if horas_semanales_grupo > settings.MAX_HORAS_SEMANALES_GRUPO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El grupo excede las horas semanales permitidas.",
        )

    for field, value in clase_actualizada.dict().items():
        setattr(clase, field, value)

    db.commit()
    db.refresh(clase)
    return clase


@router.delete("/{clase_id}", status_code=204)
def eliminar_clase_programada(clase_id: int, db: Session = Depends(get_db)):
    clase = db.query(ClaseProgramada).filter(ClaseProgramada.id == clase_id).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    db.delete(clase)
    db.commit()


@router.get("/aulas/disponibles", response_model=List[AulaResponse])
def aulas_disponibles(
    dia: DiaSemanaEnum = Query(..., description="Día de la semana"),
    hora_inicio: time = Query(..., description="Hora inicio en formato HH:MM"),
    hora_fin: time = Query(..., description="Hora fin en formato HH:MM"),
    db: Session = Depends(get_db),
):
    if hora_inicio >= hora_fin:
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser menor que la hora de fin.",
        )

    return obtener_aulas_disponibles(db, dia, hora_inicio, hora_fin)
