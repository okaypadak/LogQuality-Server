import base64

from models.OrtakBaglanti import session_scope
from models.ProjeModel import Proje
import hashlib
import time
from datetime import datetime

from util.LogProcess import logger


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

    def get_all_proje_to_dict(self, session):
        try:
            projeler = session.query(Proje).all()
            proje_listesi = []
            for proje in projeler:
                tek = {
                    'proje_id': proje.id,
                    'proje_adi': proje.proje_adi,
                    'index_name': proje.index_name,
                }
                proje_listesi.append(tek)
            return proje_listesi

        except Exception as e:
            logger.error("Error fetching projects: %s", e, exc_info=True)
            return []

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

    def generate_short_hash_id(self):
        # Zaman damgasını kullanarak benzersiz bir veri oluştur
        unique_data = str(time.time())

        # SHA-256 hash fonksiyonu kullanarak hash değerini oluştur
        hash_object = hashlib.sha256(unique_data.encode())
        hash_bytes = hash_object.digest()

        # Base64 formatına çevir
        hash_id = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')[:10]

        return hash_id
