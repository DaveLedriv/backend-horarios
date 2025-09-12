from fastapi import APIRouter

from app.enums.dia_semana import DiaSemanaEnum

router = APIRouter(prefix="/dias", tags=["Días"])


@router.get("")
def obtener_dias():
    return [d.value for d in DiaSemanaEnum]
