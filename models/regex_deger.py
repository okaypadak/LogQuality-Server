from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ortakbaglanti import SessionScope, Session
from ortakbaglanti import Base

class RegexDeger(Base):
    __tablename__ = 'regex_deger'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deger = Column(String(255), nullable=False)
    proje_id = Column(Integer, ForeignKey('proje.id'))

    # Define relationship
    proje = relationship('Proje', foreign_keys=[proje_id])

# Tabloyu veritabanına ekleyin (eğer yoksa)
# Base.metadata.create_all(bind=engine)


def create_regex_deger(session, deger, proje_id):
    new_regex_deger = RegexDeger(deger=deger, proje_id=proje_id)
    session.add(new_regex_deger)
    return new_regex_deger

def read_regex_deger(session, regex_id):
    return session.query(RegexDeger).filter_by(id=regex_id).first()

def update_regex_deger(session, regex_id, new_deger=None, new_proje_id=None):
    regex_deger = session.query(RegexDeger).filter_by(id=regex_id).first()
    if regex_deger:
        if new_deger is not None:
            regex_deger.deger = new_deger
        if new_proje_id is not None:
            regex_deger.proje_id = new_proje_id
        return regex_deger
    return None

def delete_regex_deger(session, regex_id):
    regex_deger = session.query(RegexDeger).filter_by(id=regex_id).first()
    if regex_deger:
        session.delete(regex_deger)
        return True
    return False