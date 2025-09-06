from sqlalchemy import Column, Integer, Time, Enum as PgEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.enums import DiaSemanaEnum

class DisponibilidadDocente(Base):
    __tablename__ = "disponibilidad_docente"

    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    dia = Column(PgEnum(DiaSemanaEnum), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    docente = relationship("Docente", back_populates="disponibilidades")
