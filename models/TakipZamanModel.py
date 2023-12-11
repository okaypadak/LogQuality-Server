from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.OrtakBaglanti import Base
class TakipZaman(Base):
    __tablename__ = 'takip_zaman'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    zaman = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    takip_id = Column(Integer, ForeignKey('takip.id'))

    # İlişkiyi belirtin
    takip = relationship('Takip', back_populates='takip_zaman', uselist=False)
