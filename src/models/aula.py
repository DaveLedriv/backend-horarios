from sqlalchemy import Column, Integer, String

from . import Base


class Aula(Base):
    """Representa una sala física dentro de la institución."""

    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    capacidad = Column(Integer, nullable=False)
