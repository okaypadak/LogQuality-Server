from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base

class ProjeSinif(Base):
    __tablename__ = 'proje_sinif'
    id = Column(Integer, primary_key=True)
    ad = Column(String)
    proje_id = Column(Integer, ForeignKey('proje.id'))
    proje = relationship("Proje", back_populates="proje_sinif")

    proje_metod = relationship("ProjeMetod", back_populates="proje_sinif")