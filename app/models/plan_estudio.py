from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PlanEstudio(Base):
    __tablename__ = "planes_estudio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=False)

    facultad = relationship("Facultad", back_populates="planes")
    materias = relationship(
        "Materia", back_populates="plan_estudio", cascade="all, delete"
    )
    grupos = relationship("Grupo", back_populates="plan_estudio", cascade="all, delete")

