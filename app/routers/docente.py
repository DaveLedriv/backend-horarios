from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.docente import Docente
from app.schemas.docente import DocenteCreate, DocenteResponse
from app.schemas.docente import DocenteUpdate


router = APIRouter(prefix="/docentes", tags=["Docentes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

from app.schemas.docente import DocenteUpdate

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
