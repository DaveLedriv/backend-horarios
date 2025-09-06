from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import crear_token, verificar_contrasena
from app.models.admin import Admin

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = db.query(Admin).filter(Admin.username == username).first()
    if user is None:
        raise cred_exc
    return user


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not user or not verificar_contrasena(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    access_token = crear_token(
        {"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/privado")
def ruta_privada(usuario=Depends(get_current_user)):
    return {"mensaje": f"Hola {usuario.username}"}
