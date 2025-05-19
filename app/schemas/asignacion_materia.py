from pydantic import BaseModel
from app.schemas.docente import DocenteResponse
from app.schemas.materia import MateriaResponse
from typing import Optional

class AsignacionMateriaBase(BaseModel):
    docente_id: int
    materia_id: int

class AsignacionMateriaCreate(AsignacionMateriaBase):
    pass

class AsignacionMateriaResponse(AsignacionMateriaBase):
    id: int
    docente: DocenteResponse
    materia: MateriaResponse
    class Config:
        from_attributes = True


class AsignacionMateriaUpdate(BaseModel):
    docente_id: Optional[int] = None
    materia_id: Optional[int] = None

