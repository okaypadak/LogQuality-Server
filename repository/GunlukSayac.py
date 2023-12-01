from models.GunlukSayacModel import GunlukSayac
from ortakbaglanti import Base
class GunlukSayacManager:
    def __init__(self, session):
        self.session = session

    def create_gunluk_sayac(self, tarih, satir, proje_id):
        new_gunluk_sayac = GunlukSayac(tarih=tarih, satir=satir, proje_id=proje_id)
        self.session.add(new_gunluk_sayac)
        self.session.commit()
        self.session.refresh(new_gunluk_sayac)
        return new_gunluk_sayac

    def read_gunluk_sayac(self, sayac_id):
        return self.session.query(GunlukSayac).filter_by(id=sayac_id).first()

    def update_gunluk_sayac(self, sayac_id, new_tarih=None, new_satir=None, new_proje_id=None):
        gunluk_sayac = self.session.query(GunlukSayac).filter_by(id=sayac_id).first()
        if gunluk_sayac:
            if new_tarih is not None:
                gunluk_sayac.tarih = new_tarih
            if new_satir is not None:
                gunluk_sayac.satir = new_satir
            if new_proje_id is not None:
                gunluk_sayac.proje_id = new_proje_id
            self.session.commit()
            self.session.refresh(gunluk_sayac)
            return gunluk_sayac
        return None

    def delete_gunluk_sayac(self, sayac_id):
        gunluk_sayac = self.session.query(GunlukSayac).filter_by(id=sayac_id).first()
        if gunluk_sayac:
            self.session.delete(gunluk_sayac)
            self.session.commit()
            return True
        return False