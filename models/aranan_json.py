from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ortakbaglanti import Base

class ArananJson(Base):
    __tablename__ = 'aranan_json'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aranan = Column(String(255), nullable=False)
    degisken = Column(String(255), nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    # Define relationship
    proje = relationship('Proje', foreign_keys=[proje_id])

# CRUD işlemleri
def create_aranan_json(session, aranan, degisken, proje_id):
    new_aranan_json = ArananJson(aranan=aranan, degisken=degisken, proje_id=proje_id)
    session.add(new_aranan_json)
    session.refresh(new_aranan_json)
    return new_aranan_json

def read_aranan_json(session, json_id):
    return session.query(ArananJson).filter_by(id=json_id).first()

def update_aranan_json(session, json_id, new_aranan=None, new_degisken=None, new_proje_id=None):
    aranan_json = session.query(ArananJson).filter_by(id=json_id).first()
    if aranan_json:
        if new_aranan is not None:
            aranan_json.aranan = new_aranan
        if new_degisken is not None:
            aranan_json.degisken = new_degisken
        if new_proje_id is not None:
            aranan_json.proje_id = new_proje_id
        session.refresh(aranan_json)
        return aranan_json
    return None

def delete_aranan_json(session, json_id):
    aranan_json = session.query(ArananJson).filter_by(id=json_id).first()
    if aranan_json:
        session.delete(aranan_json)
        return True
    return False
