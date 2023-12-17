from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base

class ProjeMetod(Base):
    __tablename__ = 'proje_metod'
    id = Column(Integer, primary_key=True)
    ad = Column(String)
    proje_sinif_id = Column(Integer, ForeignKey('proje_sinif.id'))
    sinif = relationship('ProjeSinif', back_populates='metodlar')