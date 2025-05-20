# app/schemas/admin.py
from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
