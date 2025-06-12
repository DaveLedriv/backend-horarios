from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.disponibilidad_docente import DisponibilidadDocenteCreate
from app.models import DisponibilidadDocente
from app.core.database import get_db
from app.schemas.disponibilidad_docente import DisponibilidadDocenteMultipleCreate

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad"])

@router.post("/", status_code=201)
def crear_disponibilidad(disponibilidad: DisponibilidadDocenteMultipleCreate, db: Session = Depends(get_db)):
    for bloque in disponibilidad.disponibles:
        nueva_disponibilidad = DisponibilidadDocente(
            docente_id=disponibilidad.docente_id,
            dia=bloque.dia,
            hora_inicio=bloque.hora_inicio,
            hora_fin=bloque.hora_fin
        )
        db.add(nueva_disponibilidad)
    db.commit()
    return {"mensaje": "Disponibilidades registradas correctamente"}