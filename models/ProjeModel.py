from sqlalchemy import Column, Integer, String

from models.OrtakBaglanti import Base


class Proje(Base):
    __tablename__ = 'proje'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proje_adi = Column(String)
    sunucu_ip = Column(String)
    sunucu_port = Column(Integer)
    kullanici_adi = Column(String)
    kullanici_sifre = Column(String)
    log_dosya_yolu = Column(String)
    secim = Column(Integer)