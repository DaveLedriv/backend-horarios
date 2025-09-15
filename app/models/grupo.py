from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    plan_estudio_id = Column(Integer, ForeignKey("planes_estudio.id"), nullable=False)
    num_estudiantes = Column(Integer, nullable=False)

    plan_estudio = relationship("PlanEstudio", back_populates="grupos")
    clases = relationship(
        "ClaseProgramada", back_populates="grupo", cascade="all, delete"
    )
