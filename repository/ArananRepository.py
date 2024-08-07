from models.Aranan import Aranan


class ArananRepository:

    def __init__(self, session):
        self.session = session

    def add_aranan(self, aciklama, adet, proje_id):
        new_record = Aranan(aciklama=aciklama, adet=adet, proje_id=proje_id)
        self.session.add(new_record)
        self.session.commit()

    def get_aranan_by_id(self, id):
        return self.session.query(Aranan).filter_by(id=id).first()

    def get_all_aranan(self):
        return self.session.query(Aranan).all()

    def update_aranan(self, id, aciklama=None, adet=None, proje_id=None):
        record = self.get_aranan_by_id(id)
        if record:
            if aciklama is not None:
                record.aciklama = aciklama
            if adet is not None:
                record.adet = adet
            if proje_id is not None:
                record.proje_id = proje_id
            self.session.commit()
        return record

    def delete_aranan(self, id):
        record = self.get_aranan_by_id(id)
        if record:
            self.session.delete(record)
            self.session.commit()
        return record
