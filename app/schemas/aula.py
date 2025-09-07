from pydantic import BaseModel
from typing import Optional


class AulaBase(BaseModel):
    nombre: str
    capacidad: Optional[int] = None


class AulaCreate(AulaBase):
    pass


class AulaResponse(AulaBase):
    id: int

    class Config:
        from_attributes = True


class AulaUpdate(BaseModel):
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
