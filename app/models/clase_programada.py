from sqlalchemy import Column, Integer, ForeignKey, Time, Enum, String
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DiaSemanaEnum(str, enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"

class ClaseProgramada(Base):
    __tablename__ = "clases_programadas"

    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    aula = Column(String, nullable=False)
    dia = Column(Enum(DiaSemanaEnum), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    docente = relationship("Docente", back_populates="clases")
    materia = relationship("Materia", back_populates="clases")
