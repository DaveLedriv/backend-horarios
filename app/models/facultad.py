from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Facultad(Base):
    __tablename__ = "facultades"
    planes = relationship(
        "PlanEstudio", back_populates="facultad", cascade="all, delete"
    )

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    docentes = relationship("Docente", back_populates="facultad", cascade="all, delete")
