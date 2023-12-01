from models.TakipModel import Takip

class TakipManager:
    def __init__(self, session):
        self.session = session

    def create_takip(self, hata, adet):
        new_takip = Takip(hata=hata, adet=adet)
        self.session.add(new_takip)
        self.session.commit()
        self.session.refresh(new_takip)
        return new_takip

    def get_takip_by_id(self, takip_id):
        return self.session.query(Takip).filter_by(id=takip_id).first()

    def get_all_takip(self):
        return self.session.query(Takip).all()

    def update_takip(self, takip_id, hata, adet):
        takip = self.session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            takip.hata = hata
            takip.adet = adet
            self.session.commit()
            self.session.refresh(takip)
        return takip

    def delete_takip(self, takip_id):
        takip = self.session.query(Takip).filter_by(id=takip_id).first()
        if takip:
            self.session.delete(takip)
            self.session.commit()
        return takip
