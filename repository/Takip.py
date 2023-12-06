from models.TakipModel import Takip

class TakipManager:

    def create_takip(self, session, hata, adet):
        new_takip = Takip(hata=hata, adet=adet)
        session.add(new_takip)
        session.commit()
        session.refresh(new_takip)
        return new_takip

    def get_takip_by_id(self, session, takip_id):
        return session.query(Takip).filter_by(id=takip_id).first()
    
    
    def get_takip_by_hata(self, session, hata):
        return session.query(Takip).filter_by(hata=hata).first()

    def get_all_takip(self, session):
        return session.query(Takip).all()

    def update_takip(self, session, takip_id, hata, adet):
        takip = session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            takip.hata = hata
            takip.adet = adet
            session.commit()
            session.refresh(takip)
        return takip

    def delete_takip(self, session, takip_id):
        takip = session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            session.delete(takip)
            session.commit()
        return takip

    def create_or_update_takip(self, session, hata):

        existing_takip = self.get_takip_by_hata(session, hata)

        if existing_takip:
            existing_takip.adet += 1
            session.refresh(existing_takip)
            return existing_takip
        else:
            # Hata yok, yeni takip oluştur
            new_takip = Takip(hata=hata, adet=1)
            session.add(new_takip)
            session.push()
            session.refresh(new_takip)
            return new_takip