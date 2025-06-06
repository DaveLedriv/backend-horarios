from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.facultad import Facultad
from app.schemas.facultad import FacultadCreate, FacultadResponse
from typing import List
from app.schemas.facultad import FacultadWithPlanes
from app.schemas.facultad import FacultadUpdate




router = APIRouter(prefix="/facultades", tags=["Facultades"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[FacultadResponse])
def listar_facultades(db: Session = Depends(get_db)):
    return db.query(Facultad).all()

@router.post("/", response_model=FacultadResponse)
def crear_facultad(facultad: FacultadCreate, db: Session = Depends(get_db)):
    db_facultad = Facultad(nombre=facultad.nombre)
    db.add(db_facultad)
    try:
        db.commit()
        db.refresh(db_facultad)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nombre duplicado o error de base de datos")
    return db_facultad

@router.get("/{facultad_id}/planes-estudio", response_model=FacultadWithPlanes)
def obtener_planes_por_facultad(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return facultad

from app.schemas.facultad import FacultadWithDocentes

@router.get("/{facultad_id}/docentes", response_model=FacultadWithDocentes)
def obtener_docentes_por_facultad(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return facultad


@router.put("/{facultad_id}", response_model=FacultadResponse)
def actualizar_facultad(facultad_id: int, datos: FacultadUpdate, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(facultad, key, value)

    db.commit()
    db.refresh(facultad)
    return facultad


@router.delete("/{facultad_id}", status_code=204)
def eliminar_facultad(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    db.delete(facultad)
    db.commit()


@router.get("/{facultad_id}", response_model=FacultadResponse)
def obtener_facultad(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return facultad


