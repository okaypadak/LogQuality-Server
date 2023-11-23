from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ortakbaglanti import Base

class Proje(Base):
    __tablename__ = 'proje'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad = Column(String(255), nullable=False)
    ip = Column(String(255), nullable=False)
    secim = Column(Integer)


# Tabloyu veritabanına ekleyin (eğer yoksa)
# Base.metadata.create_all(bind=engine)

# CRUD işlemleri için fonksiyonlar
def create_proje(session, ad, ip, secim):
    new_proje = Proje(ad=ad, ip=ip, secim=secim)
    session.add(new_proje)
    session.flush()
    return new_proje

def read_proje(session, proje_id):
    return session.query(Proje).filter_by(id=proje_id).first()

def update_proje(session, proje_id, new_ad=None, new_ip=None, new_secim=None):
    proje = session.query(Proje).filter_by(id=proje_id).first()
    if proje:
        if new_ad is not None:
            proje.ad = new_ad
        if new_ip is not None:
            proje.ip = new_ip
        if new_secim is not None:
            proje.secim = new_secim
        return proje
    return None

def delete_proje(session, proje_id):
    proje = session.query(Proje).filter_by(id=proje_id).first()
    if proje:
        session.delete(proje)
        return True
    return False