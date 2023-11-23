from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ortakbaglanti import Base

class JsonDeger(Base):
    __tablename__ = 'json_deger'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deger = Column(String(255), nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    # Define relationship
    proje = relationship('Proje', foreign_keys=[proje_id])

# Tabloyu veritabanına ekleyin (eğer yoksa)
# Base.metadata.create_all(bind=engine)

def create_json_deger(session, deger, proje_id):
    new_json_deger = JsonDeger(deger=deger, proje_id=proje_id)
    session.add(new_json_deger)
    return new_json_deger

def read_json_deger(session, json_id):
    return session.query(JsonDeger).filter_by(id=json_id).first()

def update_json_deger(session, json_id, new_deger=None, new_proje_id=None):
    json_deger = session.query(JsonDeger).filter_by(id=json_id).first()
    if json_deger:
        if new_deger is not None:
            json_deger.deger = new_deger
        if new_proje_id is not None:
            json_deger.proje_id = new_proje_id
        session.commit()
        return json_deger
    return None

def delete_json_deger(session, json_id):
    json_deger = session.query(JsonDeger).filter_by(id=json_id).first()
    if json_deger:
        session.delete(json_deger)
        return True
    return False
