from datetime import time
from pydantic import BaseModel, Field, validator
from app.enums import DiaSemanaEnum


class ClaseProgramadaBase(BaseModel):
    docente_id: int = Field(..., gt=0)
    materia_id: int = Field(..., gt=0)
    aula: str
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

    @validator("hora_fin")
    def validar_horario(cls, fin, values):
        inicio = values.get("hora_inicio")
        if inicio and fin <= inicio:
            raise ValueError("La hora de fin debe ser mayor que la de inicio")
        return fin


class ClaseProgramadaCreate(ClaseProgramadaBase):
    pass


class ClaseProgramadaUpdate(ClaseProgramadaBase):
    pass


class ClaseProgramadaResponse(ClaseProgramadaBase):
    id: int

    class Config:
        from_attributes = True
