from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import facultad, plan_estudio
from app.routers import materia
from app.routers import docente
from app.routers import asignacion_materia
from app.routers import clase_programada
from app.routers import horarios
from app.routers import disponibilidad  # <-- ✅ ESTE ES NUEVO
from app.routers import dias  # <-- ✅ ESTE ES NUEVO
from app.routers import aula
from app.routers.auth import auth_router


def create_app():
    app = FastAPI(title="Sistema de Horarios Universitarios")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(facultad.router)
    app.include_router(plan_estudio.router)
    app.include_router(materia.router)
    app.include_router(docente.router)
    app.include_router(asignacion_materia.router)
    app.include_router(clase_programada.router)
    app.include_router(aula.router)
    app.include_router(horarios.router)
    app.include_router(disponibilidad.router)  # <-- ✅ AQUÍ LO AÑADES
    app.include_router(dias.router)
    app.include_router(auth_router)

    return app


app = create_app()
