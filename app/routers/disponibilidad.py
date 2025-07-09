from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.disponibilidad_docente import DisponibilidadDocenteCreate
from app.models import DisponibilidadDocente
from app.core.database import get_db
from app.schemas.disponibilidad_docente import DisponibilidadDocenteMultipleCreate
from app.services.disponibilidad_docente import obtener_bloques_disponibles_registrados
from app.schemas.disponibilidad_docente import DisponibilidadDocenteResponse, BloqueDisponible


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
@router.put("/{disponibilidad_id}", status_code=200)
def actualizar_disponibilidad(disponibilidad_id: int, datos: DisponibilidadDocenteCreate, db: Session = Depends(get_db)):
    disponibilidad = db.query(DisponibilidadDocente).filter(DisponibilidadDocente.id == disponibilidad_id).first()
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")

    disponibilidad.dia = datos.dia
    disponibilidad.hora_inicio = datos.hora_inicio
    disponibilidad.hora_fin = datos.hora_fin
    disponibilidad.docente_id = datos.docente_id

    db.commit()
    db.refresh(disponibilidad)
    return {"mensaje": "Disponibilidad actualizada correctamente"}

@router.delete("/{disponibilidad_id}", status_code=204)
def eliminar_disponibilidad(disponibilidad_id: int, db: Session = Depends(get_db)):
    disponibilidad = db.query(DisponibilidadDocente).filter(DisponibilidadDocente.id == disponibilidad_id).first()
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")

    db.delete(disponibilidad)
    db.commit()
    return


@router.get("/docente/{docente_id}", response_model=DisponibilidadDocenteResponse)
def listar_disponibilidad_registrada(docente_id: int, db: Session = Depends(get_db)):
    bloques = db.query(DisponibilidadDocente).filter(DisponibilidadDocente.docente_id == docente_id).all()
    if not bloques:
        raise HTTPException(status_code=404, detail="No hay disponibilidad registrada para este docente")

    return {
        "docente_id": docente_id,
        "disponibles": [
            {
                "id": bloque.id,
                "dia": bloque.dia,
                "hora_inicio": bloque.hora_inicio,
                "hora_fin": bloque.hora_fin
            } for bloque in bloques
        ]
    }


@router.get("/docente/{docente_id}", response_model=DisponibilidadDocenteResponse)
def obtener_disponibilidad_registrada(docente_id: int, db: Session = Depends(get_db)):
    bloques = db.query(DisponibilidadDocente).filter(DisponibilidadDocente.docente_id == docente_id).all()

    if not bloques:
        raise HTTPException(status_code=404, detail="No hay disponibilidad registrada para este docente")

    disponibles = [
        BloqueDisponible(
            dia=bloque.dia,
            hora_inicio=bloque.hora_inicio,
            hora_fin=bloque.hora_fin
        )
        for bloque in bloques
    ]

    r