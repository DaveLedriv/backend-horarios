from sqlalchemy import Column, Integer, ForeignKey, Time, Enum, and_
from sqlalchemy.orm import relationship, foreign
from app.core.database import Base
from app.enums import DiaSemanaEnum
from app.models.timestamp_mixin import TimestampMixin

class ClaseProgramada(TimestampMixin, Base):
    __tablename__ = "clases_programadas"

    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    aula_id = Column(Integer, ForeignKey("aulas.id"), nullable=False)
    dia = Column(Enum(DiaSemanaEnum), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    docente = relationship("Docente", back_populates="clases")
    materia = relationship("Materia", back_populates="clases")
    aula = relationship("Aula", back_populates="clases")
    asignacion = relationship(
        "AsignacionMateria",
        primaryjoin=
        "and_(ClaseProgramada.docente_id==foreign(AsignacionMateria.docente_id), "
        "ClaseProgramada.materia_id==foreign(AsignacionMateria.materia_id))",
        viewonly=True,
        uselist=False,
    )
