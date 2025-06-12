from pydantic import BaseModel
from datetime import time
from typing import List
from enum import Enum

class DiaSemanaEnum(str, Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"

class BloqueDisponible(BaseModel):
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

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
