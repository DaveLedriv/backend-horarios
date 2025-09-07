from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import time

from app.enums import DiaSemanaEnum
from app.services.aulas_disponibles import obtener_aulas_disponibles
from app.schemas.clase_programada import (
    ClaseProgramadaCreate,
    ClaseProgramadaUpdate,
    ClaseProgramadaResponse,
)
from app.schemas.aula import AulaResponse
from app.models.clase_programada import ClaseProgramada
from app.core.database import get_db
from app.services import verificar_conflictos

router = APIRouter(prefix="/clases-programadas", tags=["Clases Programadas"])


@router.get("/", response_model=List[ClaseProgramadaResponse])
def listar_clases_programadas(db: Session = Depends(get_db)):
    return db.query(ClaseProgramada).all()


@router.post("/", response_model=ClaseProgramadaResponse)
def crear_clase_programada(clase: ClaseProgramadaCreate, db: Session = Depends(get_db)):
    conflicto = verificar_conflictos(
        db=db,
        docente_id=clase.docente_id,
        aula_id=clase.aula_id,
        dia=clase.dia,
        hora_inicio=clase.hora_inicio,
        hora_fin=clase.hora_fin,
        materia_id=clase.materia_id,
    )

    if conflicto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflicto detectado con otra clase en horario o aula.",
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

    conflicto = verificar_conflictos(
        db=db,
        docente_id=clase_actualizada.docente_id,
        aula_id=clase_actualizada.aula_id,
        dia=clase_actualizada.dia,
        hora_inicio=clase_actualizada.hora_inicio,
        hora_fin=clase_actualizada.hora_fin,
        materia_id=clase_actualizada.materia_id,
        clase_id_ignorar=clase_id,
    )

    if conflicto:
        raise HTTPException(
            status_code=400, detail="Conflicto detectado con otra clase"
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
