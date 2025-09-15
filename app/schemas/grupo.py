from typing import Optional

from pydantic import BaseModel, Field


class GrupoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    plan_estudio_id: int = Field(..., gt=0)
    num_estudiantes: int = Field(..., ge=0)


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    plan_estudio_id: Optional[int] = Field(None, gt=0)
    num_estudiantes: Optional[int] = Field(None, ge=0)


class GrupoResponse(GrupoBase):
    id: int

    class Config:
        from_attributes = True
