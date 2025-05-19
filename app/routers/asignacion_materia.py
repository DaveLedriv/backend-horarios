from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.asignacion_materia import AsignacionMateria
from app.models.docente import Docente
from app.schemas.asignacion_materia import AsignacionMateriaCreate, AsignacionMateriaResponse
from sqlalchemy.orm import joinedload


router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

@router.get("/", response_model=List[AsignacionMateriaResponse])
def listar_asignaciones(db: Session = Depends(get_db)):
    return db.query(AsignacionMateria).options(
        joinedload(AsignacionMateria.docente),
        joinedload(AsignacionMateria.materia)
    ).all()

@router.post("/", response_model=AsignacionMateriaResponse)
def crear_asignacion(asignacion: AsignacionMateriaCreate, db: Session = Depends(get_db)):
    existe = db.query(AsignacionMateria).filter_by(
        docente_id=asignacion.docente_id,
        materia_id=asignacion.materia_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Esta asignación ya existe")

    nueva = AsignacionMateria(**asignacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/docente/{docente_id}", response_model=List[AsignacionMateriaResponse])
def obtener_asignaciones_docente(docente_id: int, db: Session = Depends(get_db)):
    return db.query(AsignacionMateria).options(
        joinedload(AsignacionMateria.docente),
        joinedload(AsignacionMateria.materia)
    ).filter_by(docente_id=docente_id).all()

from app.schemas.asignacion_materia import AsignacionMateriaUpdate

@router.put("/{asignacion_id}", response_model=AsignacionMateriaResponse)
def actualizar_asignacion(asignacion_id: int, datos: AsignacionMateriaUpdate, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionMateria).filter_by(id=asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(asignacion, key, value)

    db.commit()
    db.refresh(asignacion)
    return asignacion

@router.delete("/{asignacion_id}", status_code=204)
def eliminar_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionMateria).filter_by(id=asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    db.delete(asignacion)
    db.commit()



