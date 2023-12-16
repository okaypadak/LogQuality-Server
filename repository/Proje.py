import base64

from models.ProjeModel import Proje
from models.GunlukSayacModel import GunlukSayac
import hashlib
import time

# CRUD işlemleri için fonksiyonlar
from datetime import datetime

from repository.GunlukSayac import GunlukSayacManager
from repository.Takip import TakipManager


class ProjeManager:

    def create_proje(self, session, proje_adi, sunucu_ip, sunucu_port, kullanici_adi, kullanici_sifre, log_dosya_yolu, secim, git_url):
        new_proje = Proje(
            proje_adi=proje_adi,
            sunucu_ip=sunucu_ip,
            sunucu_port=sunucu_port,
            kullanici_adi=kullanici_adi,
            kullanici_sifre=kullanici_sifre,
            log_dosya_yolu=log_dosya_yolu,
            secim=secim,
            git_url=git_url,
            hash_id=self.generate_short_hash_id(),
            aktif=1
        )

        session.add(new_proje)
        session.push()
        # session.refresh(new_proje)

        return new_proje

    def get_all_projeler(self, session):
        return session.query(Proje).all()

    def get_proje_by_id(self, session, proje_id):
        return session.query(Proje).filter(Proje.id == proje_id).first()

    def get_all_proje_sayac(self, session):

        gunlukSayacManager = GunlukSayacManager()

        today_date = int(datetime.now().strftime('%Y%m%d'))

        projeler = session.query(Proje).all()

        for proje in projeler:
            gunlukSayacManager.control_and_create(session, proje.id, today_date)

        gelen_projeler = (
            session.query(Proje, GunlukSayac)
            .join(GunlukSayac, Proje.id == GunlukSayac.proje_id)
            .filter(GunlukSayac.tarih == today_date)
            .all()
        )

        proje_listesi = []

        for proje, gunluk_sayac in gelen_projeler:
            proje_dict = {
                'proje_id': proje.id,
                'proje_adi': proje.proje_adi,
                'sunucu_ip': proje.sunucu_ip,
                'sunucu_port': proje.sunucu_port,
                'secim': proje.secim,
                'log_dosya_yolu': proje.log_dosya_yolu,
                'kullanici_adi': proje.kullanici_adi,
                'kullanici_sifre': proje.kullanici_sifre,
                'gunluk_sayac_id': gunluk_sayac.id,
                'sira': gunluk_sayac.sira
            }

            proje_listesi.append(proje_dict)

        return proje_listesi

    def update_proje(self, session, proje_id, new_values):
        proje = session.query(Proje).filter(Proje.id == proje_id).first()
        for key, value in new_values.items():
            setattr(proje, key, value)
        session.commit()
        return proje

    def delete_proje(self, session, proje_id):
        proje = session.query(Proje).filter_by(id=proje_id).first()
        if proje:
            session.delete(proje)
            return True
        return False

    def create_gunluk_sayac(self, session, proje_id, tarih, sayac):
        new_gunluk_sayac = GunlukSayac(proje_id=proje_id, tarih=tarih, sayac=sayac)
        session.add(new_gunluk_sayac)
        session.commit()
        session.refresh(new_gunluk_sayac)
        return new_gunluk_sayac

    def generate_short_hash_id(self):
        # Zaman damgasını kullanarak benzersiz bir veri oluştur
        unique_data = str(time.time())

        # SHA-256 hash fonksiyonu kullanarak hash değerini oluştur
        hash_object = hashlib.sha256(unique_data.encode())
        hash_bytes = hash_object.digest()

        # Base64 formatına çevir
        hash_id = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')[:10]

        return hash_id
