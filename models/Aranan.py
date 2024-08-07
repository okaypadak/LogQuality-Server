from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base

class Aranan(Base):
    __tablename__ = 'aranan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aciklama = Column(String, nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))
    proje = relationship("Proje", back_populates="aranan")

    aranan_regex = relationship("ArananRegex", back_populates="aranan")
    aranan_json = relationship("ArananJson", back_populates="aranan")
    aranan_kayit = relationship("ArananKayit", back_populates="aranan")