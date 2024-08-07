from models.ArananKayit import ArananKayit


class ArananKayitRepository:

    def __init__(self, session):
        self.session = session

    def add_aranan_kayit(self, degisken, deger, aranan_id):
        new_record = ArananKayit(degisken=degisken, deger=deger, aranan_id=aranan_id)
        self.session.add(new_record)
        self.session.commit()

    def get_aranan_kayit_by_id(self, id):
        return self.session.query(ArananKayit).filter_by(id=id).first()

    def update_aranan_kayit(self, id, degisken=None, deger=None, aranan_id=None):
        record = self.get_aranan_kayit_by_id(id)
        if record:
            if degisken is not None:
                record.degisken = degisken
            if deger is not None:
                record.deger = deger
            if aranan_id is not None:
                record.aranan_id = aranan_id
            self.session.commit()
        return record

    def delete_aranan_kayit(self, id):
        record = self.get_aranan_kayit_by_id(id)
        if record:
            self.session.delete(record)
            self.session.commit()
        return record
