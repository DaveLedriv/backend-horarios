from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.clase_programada import ClaseProgramada
from app.models.docente import Docente
from app.schemas.docente import HorarioDocenteResponse, ClaseHorario
from fastapi.responses import StreamingResponse
from app.services.exportar_excel import generar_excel_horario


router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/docente/{docente_id}", response_model=HorarioDocenteResponse)
def obtener_horario_docente(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    clases = (
        db.query(ClaseProgramada)
        .filter(ClaseProgramada.docente_id == docente_id)
        .all()
    )

    clases_formateadas = [
        ClaseHorario(
            materia=clase.materia.nombre,
            aula=clase.aula,
            dia=clase.dia,
            hora_inicio=clase.hora_inicio,
            hora_fin=clase.hora_fin,
        )
        for clase in clases
    ]

    return HorarioDocenteResponse(docente_id=docente_id, clases=clases_formateadas)

@router.get("/docente/{docente_id}/excel")
def exportar_horario_excel(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    clases = (
        db.query(ClaseProgramada)
        .filter(ClaseProgramada.docente_id == docente_id)
        .all()
    )

    excel_file = generar_excel_horario(clases, docente.nombre)

    return StreamingResponse(
        content=excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="horario_{docente.nombre}.xlsx"'
        },
    )