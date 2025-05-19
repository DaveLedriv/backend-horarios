from pydantic import BaseModel
from typing import Optional


class MateriaBase(BaseModel):
    nombre: str
    codigo: str
    creditos: int
    tipo: Optional[str] = None
    plan_estudio_id: int

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int

    class Config:
        from_attributes = True

class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    creditos: Optional[int] = None
    tipo: Optional[str] = None
    plan_estudio_id: Optional[int] = None
