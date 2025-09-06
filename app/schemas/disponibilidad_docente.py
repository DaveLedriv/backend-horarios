from pydantic import BaseModel
from datetime import time
from typing import List, Optional
from app.enums import DiaSemanaEnum


class BloqueDisponible(BaseModel):
    id: Optional[int]  # ← ID necesario para edición/eliminación
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

    class Config:
        orm_mode = True


class DisponibilidadDocenteBase(BaseModel):
    docente_id: int
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time


class DisponibilidadDocenteCreate(DisponibilidadDocenteBase):
    pass


class DisponibilidadDocenteResponse(BaseModel):
    docente_id: int
    disponibles: List[BloqueDisponible]


class DisponibilidadDocenteMultipleCreate(BaseModel):
    docente_id: int
    disponibles: List[BloqueDisponible]
