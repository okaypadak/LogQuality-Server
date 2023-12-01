from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from ortakbaglanti import Base
class GunlukSayac(Base):
    __tablename__ = 'gunluk_sayac'

    id = Column(Integer, primary_key=True, index=True)
    tarih = Column(Integer)
    satir = Column(BigInteger)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    proje = relationship('Proje', foreign_keys=[proje_id])

def get_or_create_gunluk_sayac(session, proje_id, tarih):

    existing_record = session.query(GunlukSayac).filter_by(proje_id=proje_id, tarih=tarih).first()

    if existing_record:
        return existing_record
    else:
        new_record = GunlukSayac(proje_id=proje_id, tarih=tarih, satir=0)
        session.add(new_record)
        session.commit()
        session.refresh(new_record)
        return new_record

def update_gunluk_sayac(session, proje_id, tarih):
    record = get_or_create_gunluk_sayac(proje_id, tarih)
    record.satir += 1
    session.commit()