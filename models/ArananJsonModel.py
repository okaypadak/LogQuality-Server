from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base

class ArananJson(Base):
    __tablename__ = 'aranan_json'

    id = Column(Integer, primary_key=True, autoincrement=True)
    degisken = Column(String, nullable=False)
    deger = Column(String, nullable=False)
    aranan_id = Column(Integer, ForeignKey('aranan.id'))

    aranan = relationship("Aranan", back_populates="aranan_json")