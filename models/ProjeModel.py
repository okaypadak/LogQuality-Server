from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.OrtakBaglanti import Base


class Proje(Base):
    __tablename__ = 'proje'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proje_adi = Column(String)
    index_name = Column(String)
    git_url = Column(String)
    aktif = Column(Integer)

    proje_sinif = relationship("ProjeSinif", back_populates="proje")
    aranan = relationship("Aranan", back_populates="proje")