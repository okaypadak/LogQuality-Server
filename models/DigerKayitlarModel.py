from sqlalchemy import Column, Integer, String
from models.OrtakBaglanti import Base

# Tablo sınıfını tanımla
class DigerKayitlar(Base):
    __tablename__ = 'diger_kayitlar'

    id = Column(Integer, primary_key=True, index=True)
    degisken = Column(String, nullable=True)
    deger = Column(String, nullable=True)

