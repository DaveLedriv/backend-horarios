from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate, MateriaResponse
from app.schemas.materia import MateriaUpdate


router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/", response_model=List[MateriaResponse])
def listar_materias(db: Session = Depends(get_db)):
    return db.query(Materia).all()

@router.post("/", response_model=MateriaResponse)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    nueva = Materia(**materia.dict())
    db.add(nueva)
    try:
        db.commit()
        db.refresh(nueva)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Código duplicado u error de BD")
    return nueva

@router.put("/{materia_id}", response_model=MateriaResponse)
def actualizar_materia(materia_id: int, datos: MateriaUpdate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(materia, key, value)

    try:
        db.commit()
        db.refresh(materia)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar la materia")

    return materia

@router.delete("/{materia_id}", status_code=204)
def eliminar_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    db.delete(materia)
    db.commit()

@router.get("/{materia_id}", response_model=MateriaResponse)
def obtener_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia

