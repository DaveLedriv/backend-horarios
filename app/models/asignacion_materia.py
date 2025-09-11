from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class AsignacionMateria(Base):
    __tablename__ = "asignaciones_materia"
    __table_args__ = (UniqueConstraint('docente_id', 'materia_id', name='uix_docente_materia'),)

    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)

    docente = relationship("Docente", back_populates="asignaciones")
    materia = relationship("Materia", back_populates="asignaciones")

    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
