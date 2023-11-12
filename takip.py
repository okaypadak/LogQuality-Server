from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://admin:1234@localhost:5432/logstrack')
Base = declarative_base()

class takip(Base):
    __tablename__ = 'takip'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarih = Column(Date)
    sinif = Column(String(collation='default'))
    metod = Column(String(collation='default'))
    hata = Column(String(collation='default'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_entry(date, class_name, method, error):
    new_entry = takip(tarih=date, sinif=class_name, metod=method, hata=error)
    session.add(new_entry)
    session.commit()
    print(f"Yeni eklenen girişin ID'si: {new_entry.id}")

def read_all_entries():
    all_entries = session.query(takip).all()
    for entry in all_entries:
        print(f"ID: {entry.id}, Tarih: {entry.tarih}, Sınıf: {entry.sinif}, Metod: {entry.metod}, Hata: {entry.hata}")

def update_entry(entry_id, new_error):
    entry_to_update = session.query(takip).filter_by(id=entry_id).first()
    if entry_to_update:
        entry_to_update.hata = new_error
        session.commit()

def delete_entry(entry_id):
    entry_to_delete = session.query(takip).filter_by(id=entry_id).first()
    if entry_to_delete:
        session.delete(entry_to_delete)
        session.commit()
