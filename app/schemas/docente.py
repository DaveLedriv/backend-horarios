from pydantic import BaseModel, EmailStr
from typing import Optional

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
        orm_mode = True


class DocenteUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    numero_empleado: Optional[str] = None
    facultad_id: Optional[int] = None
