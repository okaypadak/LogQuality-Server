from models.TakipModel import Takip

class TakipManager:

    def create_takip(self, session, hata, adet):
        new_takip = Takip(hata=hata, adet=adet)
        session.add(new_takip)
        return new_takip

    def get_takip_by_id(self, session, takip_id):
        return session.query(Takip).filter_by(id=takip_id).first()

    @staticmethod
    def get_takip_by_hata(session, nerde, hata, proje_id):
        return session.query(Takip).filter_by(nerde=nerde, hata=hata, proje_id=proje_id).first()

    def get_all_takip(self, session):
        return session.query(Takip).all()

    def update_takip(self, session, takip_id, hata, adet):
        takip = session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            takip.hata = hata
            takip.adet = adet
        return takip

    def delete_takip(self, session, takip_id):
        takip = session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            session.delete(takip)
        return takip

    @staticmethod
    def create_or_update_takip(session, nerde, hata, projeId):

        existing_takip = TakipManager.get_takip_by_hata(session, nerde, hata, projeId)

        if existing_takip:
            existing_takip.adet += 1
            return existing_takip
        else:
            # Hata yok, yeni takip oluştur
            new_takip = Takip(nerde=nerde, hata=hata, adet=1, proje_id=projeId)
            session.add(new_takip)
            session.flush()
            return new_takip