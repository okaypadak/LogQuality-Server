from datetime import datetime, timezone

from models.ProjeMetodModel import ProjeMetod
from models.ProjeSinifModel import ProjeSinif
from models.TakipZamanModel import TakipZaman


class ProjeSinifMetodManager:
    # CREATE işlemleri
    def create_proje_sinif(self, session, class_name, project_id):
        proje_sinif = ProjeSinif(ad=class_name, proje_id=project_id)
        session.add(proje_sinif)
        session.flush()  # primary key almak için
        return proje_sinif.id

    def create_proje_metod(self, session, method_name, proje_sinif_id):
        proje_metod = ProjeMetod(ad=method_name, proje_sinif_id=proje_sinif_id)
        session.add(proje_metod)
        session.commit()
        return proje_metod.id

    # READ işlemleri
    def get_proje_sinif_id(self, session, sinif_id):
        return session.query(ProjeSinif).get(sinif_id)

    def get_proje_sinif_proje_id(self, session, proje_id):
        return session.query(ProjeSinif).filter_by(proje_id=proje_id).delete()

    def get_proje_metod(self, session, metod_id):
        return session.query(ProjeMetod).get(metod_id)

    # UPDATE işlemleri
    def update_proje_sinif(self, session, sinif_id, new_class_name):
        proje_sinif = self.get_proje_sinif(sinif_id)
        if proje_sinif:
            proje_sinif.ad = new_class_name
            session.commit()

    def update_proje_metod(self, session, metod_id, new_method_name):
        proje_metod = self.get_proje_metod(metod_id)
        if proje_metod:
            proje_metod.ad = new_method_name
            session.commit()

    # DELETE işlemleri
    def delete_proje_sinif(self, session, sinif_id):
        proje_sinif = self.get_proje_sinif(session, sinif_id)
        if proje_sinif:
            session.delete(proje_sinif)

    def delete_proje_metod(self, session, metod_id):
        proje_metod = self.get_proje_metod(metod_id)
        if proje_metod:
            session.delete(proje_metod)
            session.commit()

    def create_list(self, session, data, project_id):

        self.get_proje_sinif_proje_id(session, project_id)

        for class_list in data:
            for class_data in class_list:
                class_name = class_data['class_name']
                methods = class_data['method_names']

                # ProjeSinif tablosuna ekleme
                sinif_id = self.create_proje_sinif(session, class_name, project_id)

                # ProjeMetod tablosuna ekleme
                for method_name in methods:
                    self.create_proje_metod(session, method_name, sinif_id)