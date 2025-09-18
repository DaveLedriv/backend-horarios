from datetime import time, datetime
from typing import List

from pydantic import BaseModel, Field, validator

from app.enums import DiaSemanaEnum
from app.schemas.asignacion_materia import AsignacionMateriaResponse
from app.schemas.aula import AulaResponse
from app.schemas.grupo import GrupoResponse


class ClaseProgramadaBase(BaseModel):
    docente_id: int = Field(..., gt=0)
    materia_id: int = Field(..., gt=0)
    aula_id: int = Field(..., gt=0)
    grupo_id: int = Field(..., gt=0)
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
            valor = value.strip()
            formatos = [
                ("%I:%M %p", valor.upper()),
                ("%H:%M", valor),
                ("%H:%M:%S", valor),
            ]

            for formato, valor_a_parsear in formatos:
                try:
                    return datetime.strptime(valor_a_parsear, formato).time()
                except ValueError:
                    continue

            raise ValueError(
                "Formato de hora inválido. Use uno de los formatos válidos: "
                "HH:MM AM/PM, HH:MM (24h), HH:MM:SS (24h)"
            )
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


class ClaseProgramadaDetalle(ClaseProgramadaResponse):
    asignacion: AsignacionMateriaResponse
    aula: AulaResponse
    grupo: GrupoResponse

    class Config:
        from_attributes = True
