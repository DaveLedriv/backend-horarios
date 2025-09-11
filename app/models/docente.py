from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    numero_empleado = Column(String(20), nullable=False, unique=True)

    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=False)
    facultad = relationship("Facultad", back_populates="docentes")
    asignaciones = relationship("AsignacionMateria", back_populates="docente", cascade="all, delete")
    clases = relationship("ClaseProgramada", back_populates="docente")
    disponibilidades = relationship("DisponibilidadDocente", back_populates="docente", cascade="all, delete")

    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

