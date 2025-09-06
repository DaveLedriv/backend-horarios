from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import time

from app.core.database import get_db
from app.models.docente import Docente
from app.schemas.docente import (
    DocenteCreate,
    DocenteResponse,
    DocenteUpdate,
    DisponibilidadDocenteResponse,
    BloqueDisponible,
)
from app.services.disponibilidad_docente import obtener_disponibilidad_docente
from app.enums import DiaSemanaEnum


router = APIRouter(prefix="/docentes", tags=["Docentes"])

@router.get("/", response_model=List[DocenteResponse])
def listar_docentes(db: Session = Depends(get_db)):
    return db.query(Docente).all()

@router.post("/", response_model=DocenteResponse)
def crear_docente(docente: DocenteCreate, db: Session = Depends(get_db)):
    nuevo = Docente(**docente.dict())
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Correo o número de empleado duplicado")
    return nuevo

@router.put("/{docente_id}", response_model=DocenteResponse)
def actualizar_docente(docente_id: int, datos: DocenteUpdate, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(docente, key, value)

    try:
        db.commit()
        db.refresh(docente)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el docente")

    return docente

@router.delete("/{docente_id}", status_code=204)
def eliminar_docente(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if docente is None:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    db.delete(docente)
    db.commit()


@router.get("/{docente_id}/disponibilidad", response_model=DisponibilidadDocenteResponse)
def consultar_disponibilidad(
    docente_id: int,
    dia: DiaSemanaEnum = Query(None, description="Día de la semana, ej: lunes"),
    desde: time = Query(None, description="Hora mínima de inicio, formato HH:MM"),
    hasta: time = Query(None, description="Hora máxima de fin, formato HH:MM"),
    db: Session = Depends(get_db)
):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    bloques = obtener_disponibilidad_docente(db, docente_id, dia, desde, hasta)

    return DisponibilidadDocenteResponse(
        docente_id=docente_id,
        disponibles=[BloqueDisponible(**b) for b in bloques]
    )
@router.get("/{docente_id}", response_model=DocenteResponse)
def obtener_docente(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente
