from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base

def create_app():
    app = FastAPI(title="Sistema de Horarios Universitarios")

    # Aquí se pueden incluir routers más adelante
    # app.include_router(...)

    return app

app = create_app()
