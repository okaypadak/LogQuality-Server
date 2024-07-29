from datetime import datetime, timezone
from models.TakipZamanModel import TakipZaman


class TakipZamanManager:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def create_takip_zaman(session, logId, takipId, zaman=None):
        if zaman is None:
            zaman = datetime.now(timezone.utc)

        new_takip_zaman = TakipZaman(log_id=logId, zaman=zaman, takip_id=takipId)
        session.add(new_takip_zaman)
        session.commit()
        session.refresh(new_takip_zaman)
        return new_takip_zaman

    def get_takip_zaman_by_id(self, takip_zaman_id):
        return self.session.query(TakipZaman).filter_by(id=takip_zaman_id).first()

    def get_all_takip_zaman(self):
        return self.session.query(TakipZaman).all()

    def update_takip_zaman(self, takip_zaman_id, takip_id):
        takip_zaman = self.session.query(TakipZaman).filter_by(id=takip_zaman_id).first()
        if takip_zaman:
            takip_zaman.takip_id = takip_id
            self.session.commit()
            self.session.refresh(takip_zaman)
        return takip_zaman

    def delete_takip_zaman(self, takip_zaman_id):
        takip_zaman = self.session.query(TakipZaman).filter_by(id=takip_zaman_id).first()
        if takip_zaman:
            self.session.delete(takip_zaman)
            self.session.commit()
        return takip_zaman
