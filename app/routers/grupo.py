from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.grupo import Grupo
from app.schemas.grupo import GrupoCreate, GrupoResponse, GrupoUpdate

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.get("/", response_model=List[GrupoResponse])
def listar_grupos(db: Session = Depends(get_db)):
    return db.query(Grupo).all()


@router.get("/{grupo_id}", response_model=GrupoResponse)
def obtener_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def crear_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    nuevo_grupo = Grupo(**grupo.dict())
    db.add(nuevo_grupo)
    db.commit()
    db.refresh(nuevo_grupo)
    return nuevo_grupo


@router.put("/{grupo_id}", response_model=GrupoResponse)
def actualizar_grupo(
    grupo_id: int, datos: GrupoUpdate, db: Session = Depends(get_db)
):
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(grupo, key, value)

    db.commit()
    db.refresh(grupo)
    return grupo


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    db.delete(grupo)
    db.commit()
