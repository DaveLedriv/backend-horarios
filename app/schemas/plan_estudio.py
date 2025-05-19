from pydantic import BaseModel
from app.schemas.materia import MateriaResponse
from typing import List
from typing import Optional

class PlanEstudioBase(BaseModel):
    nombre: str
    facultad_id: int

class PlanEstudioCreate(PlanEstudioBase):
    pass

class PlanEstudioResponse(PlanEstudioBase):
    id: int

    class Config:
        orm_mode = True

class PlanEstudioWithMaterias(BaseModel):
    id: int
    nombre: str
    facultad_id: int
    materias: List[MateriaResponse] = []

    class Config:
        orm_mode = True

class PlanEstudioUpdate(BaseModel):
    nombre: Optional[str] = None
    facultad_id: Optional[int] = None
