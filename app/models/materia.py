from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Boolean


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False, unique=True)
    creditos = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=True)

    plan_estudio_id = Column(Integer, ForeignKey("planes_estudio.id"), nullable=False)
    plan_estudio = relationship("PlanEstudio", back_populates="materias")
    asignaciones = relationship("AsignacionMateria", back_populates="materia", cascade="all, delete")
    clases = relationship("ClaseProgramada", back_populates="materia")
    permite_superposicion = Column(Boolean, default=False)
