from fastapi import FastAPI
from app.routers import facultad, plan_estudio
from app.routers import materia
from app.routers import docente
from app.routers import asignacion_materia

from app.core.config import settings
from app.core.database import engine, Base

def create_app():
    app = FastAPI(title="Sistema de Horarios Universitarios")

    app.include_router(facultad.router)
    app.include_router(plan_estudio.router)
    app.include_router(materia.router)
    app.include_router(docente.router)
    app.include_router(asignacion_materia.router)

    return app

app = create_app()
