from datetime import time, datetime
from typing import List

from pydantic import BaseModel, Field, validator

from app.enums import DiaSemanaEnum


class ClaseProgramadaBase(BaseModel):
    docente_id: int = Field(..., gt=0)
    materia_id: int = Field(..., gt=0)
    aula_id: int = Field(..., gt=0)
    dia: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

    @validator("dia", pre=True)
    def validar_dia(cls, v: str) -> DiaSemanaEnum:
        v_lower = v.lower()
        dias_validos: List[str] = [d.value for d in DiaSemanaEnum]
        if v_lower not in dias_validos:
            raise ValueError("El día no es válido")
        return DiaSemanaEnum(v_lower)

    @validator("hora_inicio", "hora_fin", pre=True)
    def parsear_hora(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip().upper(), "%I:%M %p").time()
            except ValueError:
                raise ValueError("Formato de hora inválido. Use HH:MM AM/PM")
        return value

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
