from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import time
from typing import List
from enum import Enum

class DocenteBase(BaseModel):
    nombre: str
    correo: EmailStr
    numero_empleado: str
    facultad_id: int

class DocenteCreate(DocenteBase):
    pass

class DocenteResponse(DocenteBase):
    id: int

    class Config:
        from_attributes = True


class DocenteUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    numero_empleado: Optional[str] = None
    facultad_id: Optional[int] = None

class DiaSemanaEnum(str, Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"


class ClaseHorario(BaseModel):
    materia: str
    aula: str
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

    class Config:
        orm_mode = True


class HorarioDocenteResponse(BaseModel):
    docente_id: int
    clases: List[ClaseHorario]

class BloqueDisponible(BaseModel):
    dia: str
    hora_inicio: time
    hora_fin: time

class DisponibilidadDocenteResponse(BaseModel):
    docente_id: int
    disponibles: List[BloqueDisponible]
