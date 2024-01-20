from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base

class ArananRegex(Base):
    __tablename__ = 'aranan_degex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aranan = Column(String(255), nullable=False)
    degisken = Column(String(255), nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    proje = relationship('Proje', foreign_keys=[proje_id])
