from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.plan_estudio import PlanEstudio
from app.schemas.plan_estudio import PlanEstudioCreate, PlanEstudioResponse
from app.schemas.plan_estudio import PlanEstudioWithMaterias
from app.schemas.plan_estudio import PlanEstudioUpdate


router = APIRouter(prefix="/planes-estudio", tags=["Planes de Estudio"])


@router.get("/", response_model=List[PlanEstudioResponse])
def listar_planes(db: Session = Depends(get_db)):
    return db.query(PlanEstudio).all()


@router.post("/", response_model=PlanEstudioResponse)
def crear_plan(plan: PlanEstudioCreate, db: Session = Depends(get_db)):
    db_plan = PlanEstudio(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/{plan_id}/materias", response_model=PlanEstudioWithMaterias)
def obtener_materias_por_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    return plan


@router.put("/{plan_id}", response_model=PlanEstudioResponse)
def actualizar_plan(
    plan_id: int, datos: PlanEstudioUpdate, db: Session = Depends(get_db)
):
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(plan, key, value)

    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/{plan_id}", status_code=204)
def eliminar_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")

    db.delete(plan)
    db.commit()


@router.get("/{plan_id}", response_model=PlanEstudioResponse)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan
