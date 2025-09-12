from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.clase_programada import ClaseProgramada
from app.models.docente import Docente
from app.models.aula import Aula
from app.schemas.clase_programada import ClaseProgramadaDetalle
from app.models.asignacion_materia import AsignacionMateria
from fastapi.responses import StreamingResponse
from app.services.exportar_excel import generar_excel_horario, generar_excel_horario_aula


router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/docente/{docente_id}", response_model=Dict[str, List[ClaseProgramadaDetalle]])
def obtener_horario_docente(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    clases = (
        db.query(ClaseProgramada)
        .options(
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.docente),
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.materia),
            selectinload(ClaseProgramada.aula),
        )
        .filter(ClaseProgramada.docente_id == docente_id)
        .all()
    )

    return {"clases": clases}


@router.get("/docente/{docente_id}/excel")
def exportar_horario_excel(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    clases = (
        db.query(ClaseProgramada)
        .options(
            selectinload(ClaseProgramada.docente),
            selectinload(ClaseProgramada.materia),
            selectinload(ClaseProgramada.aula),
        )
        .filter(ClaseProgramada.docente_id == docente_id)
        .all()
    )

    excel_file = generar_excel_horario(clases, docente.nombre)

    return StreamingResponse(
        content=excel_file,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="horario_{docente.nombre}.xlsx"'
            )
        },
    )


@router.get("/aula/{aula_id}", response_model=Dict[str, List[ClaseProgramadaDetalle]])
def obtener_horario_aula(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    clases = (
        db.query(ClaseProgramada)
        .options(
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.docente),
            selectinload(ClaseProgramada.asignacion)
            .selectinload(AsignacionMateria.materia),
            selectinload(ClaseProgramada.aula),
        )
        .filter(ClaseProgramada.aula_id == aula_id)
        .all()
    )

    return {"clases": clases}


@router.get("/aula/{aula_id}/excel")
def exportar_horario_aula_excel(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    clases = (
        db.query(ClaseProgramada)
        .options(
            selectinload(ClaseProgramada.docente),
            selectinload(ClaseProgramada.materia),
            selectinload(ClaseProgramada.aula),
        )
        .filter(ClaseProgramada.aula_id == aula_id)
        .all()
    )

    excel_file = generar_excel_horario_aula(clases, aula.nombre)

    return StreamingResponse(
        content=excel_file,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="horario_aula_{aula.nombre}.xlsx"'
            )
        },
    )
