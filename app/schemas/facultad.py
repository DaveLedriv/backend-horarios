from pydantic import BaseModel
from typing import List, Optional
from app.schemas.plan_estudio import PlanEstudioResponse
from app.schemas.docente import DocenteResponse
from typing import List


class FacultadBase(BaseModel):
    nombre: str

class FacultadCreate(FacultadBase):
    pass

class FacultadResponse(FacultadBase):
    id: int

    class Config:
        from_attributes = True

class FacultadWithPlanes(BaseModel):
    id: int
    nombre: str
    planes: List[PlanEstudioResponse] = []

    class Config:
        from_attributes = True

class FacultadWithDocentes(BaseModel):
    id: int
    nombre: str
    docentes: List[DocenteResponse] = []

    class Config:
        from_attributes = True



class FacultadUpdate(BaseModel):
    nombre: Optional[str] = None
