from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    capacidad = Column(Integer, nullable=True)

    clases = relationship("ClaseProgramada", back_populates="aula", cascade="all, delete")
