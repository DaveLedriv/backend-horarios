# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "superclave"  # mover a .env
ALGORITHM = "HS256"

def verificar_contrasena(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encriptar_contrasena(password):
    return pwd_context.hash(password)

def crear_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
