from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import ortakbaglanti as session
from ortakbaglanti import Base
class TakipZaman(Base):
    __tablename__ = 'takip_zaman'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    zaman = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    takip_id = Column(Integer, ForeignKey('takip.id'))

    # İlişkiyi belirtin
    takip = relationship('Takip', back_populates='takip_zaman', uselist=False)

# Tabloyu veritabanına ekleyin (eğer yoksa)
# Base.metadata.create_all(bind=engine)

# CRUD işlemleri için fonksiyonlar
def create_takip_zaman(takip_id, zaman=None):
    if zaman is None:
        zaman = datetime.now(timezone.utc)

    new_takip_zaman = TakipZaman(takip_id=takip_id, zaman=zaman)
    session.add(new_takip_zaman)
    return new_takip_zaman

def get_takip_zaman_by_id(takip_zaman_id):
    return session.query(TakipZaman).filter_by(id=takip_zaman_id).first()

def get_all_takip_zaman():
    return session.query(TakipZaman).all()

def update_takip_zaman(takip_zaman_id, takip_id):
    takip_zaman = session.query(TakipZaman).filter_by(id=takip_zaman_id).first()
    if takip_zaman:
        takip_zaman.takip_id = takip_id
    return takip_zaman

def delete_takip_zaman(takip_zaman_id):
    takip_zaman = session.query(TakipZaman).filter_by(id=takip_zaman_id).first()
    if takip_zaman:
        session.delete(takip_zaman)
    return takip_zaman
