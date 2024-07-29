from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.OrtakBaglanti import Base

class Takip(Base):
    __tablename__ = 'takip'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    nerde = Column(String)
    hata = Column(String)
    adet = Column(Integer)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    proje = relationship('Proje', foreign_keys=[proje_id])
    takip_zaman = relationship('TakipZaman', back_populates='takip',)