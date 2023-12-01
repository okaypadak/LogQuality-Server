from models.diger_kayitlar import DigerKayitlar

class DigerKayitlarCRUD:
    def create_diger_kayit(self, session, degisken, deger):
        new_diger_kayit = DigerKayitlar(degisken=degisken, deger=deger)
        session.add(new_diger_kayit)
        session.refresh(new_diger_kayit)
        return new_diger_kayit

    def read_diger_kayit(self, session, kayit_id):
        return session.query(DigerKayitlar).filter_by(id=kayit_id).first()

    def update_diger_kayit(self, session, kayit_id, new_degisken=None, new_deger=None):
        diger_kayit = session.query(DigerKayitlar).filter_by(id=kayit_id).first()
        if diger_kayit:
            if new_degisken is not None:
                diger_kayit.degisken = new_degisken
            if new_deger is not None:
                diger_kayit.deger = new_deger
            session.refresh(diger_kayit)
            return diger_kayit
        return None

    def delete_diger_kayit(self, session, kayit_id):
        diger_kayit = session.query(DigerKayitlar).filter_by(id=kayit_id).first()
        if diger_kayit:
            session.delete(diger_kayit)
            return True
        return False