from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ortakbaglanti import Base
from models.gunluk_sayac import GunlukSayac

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

# Tabloyu veritabanına ekleyin (eğer yoksa)
# Base.metadata.create_all(bind=engine)

# CRUD işlemleri için fonksiyonlar
def create_proje(session, proje_adi, sunucu_ip, sunucu_port, kullanici_adi, kullanici_sifre, log_dosya_yolu, secim):
    new_proje = Proje(
        proje_adi=proje_adi,
        sunucu_ip=sunucu_ip,
        sunucu_port=sunucu_port,
        kullanici_adi=kullanici_adi,
        kullanici_sifre=kullanici_sifre,
        log_dosya_yolu=log_dosya_yolu,
        secim=secim
    )
    session.add(new_proje)
    session.commit()

def get_all_proje(session):
    return session.query(Proje).all()

# READ
def get_proje_by_id(session, proje_id):
    return session.query(Proje).filter(Proje.id == proje_id).first()

def get_all_proje_sayac(session):
    today_date = int(datetime.now().strftime('%Y%m%d'))

    gelen_projeler = (
        session.query(Proje, GunlukSayac)
        .join(GunlukSayac, Proje.id == GunlukSayac.proje_id)
        .filter(GunlukSayac.tarih == today_date)
        .all()
    )

    proje_listesi = []

    for proje, gunluk_sayac in gelen_projeler:
        proje_dict = {
            'id': proje.id,
            'proje_adi': proje.proje_adi,
            'sunucu_ip': proje.sunucu_ip,
            'sunucu_port': proje.sunucu_port,
            'log_dosya_yolu': proje.log_dosya_yolu,
            'kullanici_adi': proje.kullanici_adi,
            'kullanici_sifre': proje.kullanici_sifre,
            'gunluk_sayac_id': gunluk_sayac.id,
            'gunluk_sayac': gunluk_sayac.sayac
        }

        proje_listesi.append(proje_dict)

    return proje_listesi

# UPDATE
def update_proje(session, proje_id, new_values):
    proje = session.query(Proje).filter(Proje.id == proje_id).first()
    for key, value in new_values.items():
        setattr(proje, key, value)

def update_proje(session, proje_id, new_adi=None, new_ip=None, new_port=None, new_kullanici_adi=None,
                 new_kullanici_sifre=None, new_log_dosya_yolu=None, new_secim=None):
    proje = session.query(Proje).filter_by(id=proje_id).first()
    if proje:
        if new_adi is not None:
            proje.proje_adi = new_adi

        if new_ip is not None:
            proje.sunucu_ip = new_ip

        if new_port is not None:
            proje.sunucu_port = new_port

        if new_kullanici_adi is not None:
            proje.kullanici_adi = new_kullanici_adi

        if new_kullanici_sifre is not None:
            proje.kullanici_sifre = new_kullanici_sifre

        if new_log_dosya_yolu is not None:
            proje.log_dosya_yolu = new_log_dosya_yolu

        if new_secim is not None:
            proje.secim = new_secim

        session.commit()
        return proje
    return None

def delete_proje(session, proje_id):
    proje = session.query(Proje).filter_by(id=proje_id).first()
    if proje:
        session.delete(proje)
        return True
    return False