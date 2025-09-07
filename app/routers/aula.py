from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.aula import Aula
from app.schemas.aula import AulaCreate, AulaResponse, AulaUpdate

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("/", response_model=List[AulaResponse])
def listar_aulas(db: Session = Depends(get_db)):
    return db.query(Aula).all()


@router.post("/", response_model=AulaResponse)
def crear_aula(aula: AulaCreate, db: Session = Depends(get_db)):
    nueva = Aula(**aula.dict())
    db.add(nueva)
    try:
        db.commit()
        db.refresh(nueva)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el aula")
    return nueva


@router.get("/{aula_id}", response_model=AulaResponse)
def obtener_aula(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.put("/{aula_id}", response_model=AulaResponse)
def actualizar_aula(aula_id: int, datos: AulaUpdate, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(aula, key, value)

    try:
        db.commit()
        db.refresh(aula)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el aula")
    return aula


@router.delete("/{aula_id}", status_code=204)
def eliminar_aula(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    db.delete(aula)
    db.commit()
