from pydantic import BaseModel
from typing import Optional, List
from datetime import time
from app.enums import DiaSemanaEnum


class AulaBase(BaseModel):
    nombre: str
    capacidad: Optional[int] = None


class AulaCreate(AulaBase):
    pass


class AulaResponse(AulaBase):
    id: int

    class Config:
        from_attributes = True


class AulaUpdate(BaseModel):
    nombre: Optional[str] = None
    capacidad: Optional[int] = None


class ClaseHorarioAula(BaseModel):
    materia: str
    docente: str
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

    class Config:
        orm_mode = True


class HorarioAulaResponse(BaseModel):
    aula_id: int
    clases: List[ClaseHorarioAula]
