from sqlalchemy import Column, Integer, String
import ortakbaglanti as session
from ortakbaglanti import Base

class Takip(Base):
    __tablename__ = 'takip'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    sinif = Column(String(255))
    metod = Column(String(255))
    hata = Column(String(255))
    adet = Column(String(255))

# CRUD işlemleri için fonksiyonlar
def create_takip(sinif, metod, hata, adet):
    new_takip = Takip(sinif=sinif, metod=metod, hata=hata, adet=adet)
    session.add(new_takip)
    return new_takip

def get_takip_by_id(takip_id):
    return session.query(Takip).filter_by(id=takip_id).first()

def get_all_takip():
    return session.query(Takip).all()

def update_takip(takip_id, sinif, metod, hata, adet):
    takip = session.query(Takip).filter_by(id=takip_id).first()
    if takip:
        takip.sinif = sinif
        takip.metod = metod
        takip.hata = hata
        takip.adet = adet
    return takip

def delete_takip(takip_id):
    takip = session.query(Takip).filter_by(id=takip_id).first()
    if takip:
        session.delete(takip)
    return takip