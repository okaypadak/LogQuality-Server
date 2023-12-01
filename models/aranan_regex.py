from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ortakbaglanti import SessionScope, Session
from ortakbaglanti import Base

class ArananRegex(Base):
    __tablename__ = 'aranan_degex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aranan = Column(String(255), nullable=False)
    degisken = Column(String(255), nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))
    # Define relationship
    proje = relationship('Proje', foreign_keys=[proje_id])

# CRUD işlemleri
def create_regex_deger(session, aranan, degisken, proje_id):
    new_regex_deger = ArananRegex(aranan=aranan, degisken=degisken, proje_id=proje_id)
    session.add(new_regex_deger)
    session.commit()
    session.refresh(new_regex_deger)
    return new_regex_deger

def read_regex_deger(session, regex_id):
    return session.query(ArananRegex).filter_by(id=regex_id).first()

def update_regex_deger(session, regex_id, new_deger=None, new_proje_id=None):
    regex_deger = session.query(ArananRegex).filter_by(id=regex_id).first()
    if regex_deger:
        if new_deger is not None:
            regex_deger.deger = new_deger
        if new_proje_id is not None:
            regex_deger.proje_id = new_proje_id
        session.commit()
        session.refresh(regex_deger)
        return regex_deger
    return None

def delete_regex_deger(session, regex_id):
    regex_deger = session.query(ArananRegex).filter_by(id=regex_id).first()
    if regex_deger:
        session.delete(regex_deger)
        session.commit()
        return True
    return False