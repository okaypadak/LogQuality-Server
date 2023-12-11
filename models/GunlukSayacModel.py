from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from models.OrtakBaglanti import Base
class GunlukSayac(Base):
    __tablename__ = 'gunluk_sayac'

    id = Column(Integer, primary_key=True, index=True)
    tarih = Column(Integer)
    sira = Column(BigInteger)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    proje = relationship('Proje', foreign_keys=[proje_id])
