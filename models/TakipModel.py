from sqlalchemy import Column, Integer, String
import ortakbaglanti as session
from ortakbaglanti import Base

class Takip(Base):
    __tablename__ = 'takip'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    hata = Column(String(255))
    adet = Column(String(255))
