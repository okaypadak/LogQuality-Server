from models.GunlukSayacModel import GunlukSayac
from util import LogProcess as log
class GunlukSayacManager:
    def control_and_create(self, session, proje_id, tarih):

        gunluk_sayac = (
            session.query(GunlukSayac)
            .filter(GunlukSayac.proje_id == proje_id, GunlukSayac.tarih == tarih)
            .first()
        )

        if gunluk_sayac:
            log.logger.info(f"Kayıt zaten mevcut: {gunluk_sayac.proje_id}")
        else:
            yeni_kayit = GunlukSayac(tarih=tarih, sira=0, proje_id=proje_id)
            session.add(yeni_kayit)
            log.logger.info(f"Yeni kayıt oluşturuldu: {yeni_kayit}")

    def create_gunluk_sayac(self, session, tarih, sira, proje_id):
        new_gunluk_sayac = GunlukSayac(tarih=tarih, sira=sira, proje_id=proje_id)
        session.add(new_gunluk_sayac)
        #session.commit()
        session.refresh(new_gunluk_sayac)
        return new_gunluk_sayac

    def read_gunluk_sayac(session, self, sayac_id):
        return session.query(GunlukSayac).filter_by(id=sayac_id).first()

    def update_gunluk_sayac(self, session, sayac_id, new_tarih=None, new_sira=None, new_proje_id=None):
        gunluk_sayac = session.query(GunlukSayac).filter_by(id=sayac_id).first()
        if gunluk_sayac:
            if new_tarih is not None:
                gunluk_sayac.tarih = new_tarih
            if new_sira is not None:
                gunluk_sayac.sira = new_sira
            if new_proje_id is not None:
                gunluk_sayac.proje_id = new_proje_id
            #session.commit()
            #session.refresh(gunluk_sayac)
            return gunluk_sayac
        return None

    def delete_gunluk_sayac(self, session, sayac_id):
        gunluk_sayac = session.query(GunlukSayac).filter_by(id=sayac_id).first()
        if gunluk_sayac:
            session.delete(gunluk_sayac)
            session.commit()
            return True
        return False