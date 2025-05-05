from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Facultad(Base):
    __tablename__ = "facultades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
