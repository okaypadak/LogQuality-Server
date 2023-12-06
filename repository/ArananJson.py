from models.ArananJsonModel import ArananJson


# CRUD işlemleri
class ArananJsonManager:

    def create_aranan_json(self, session, aranan, degisken, proje_id):
        new_aranan_json = ArananJson(aranan=aranan, degisken=degisken, proje_id=proje_id)
        session.add(new_aranan_json)
        session.refresh(new_aranan_json)
        return new_aranan_json

    def get_all_regex(self):
        return self.session.query(ArananJson).all()

    def read_aranan_json(self, json_id):
        return self.session.query(ArananJson).filter_by(id=json_id).first()

    def update_aranan_json(self, json_id, new_aranan=None, new_degisken=None, new_proje_id=None):
        aranan_json = self.session.query(ArananJson).filter_by(id=json_id).first()
        if aranan_json:
            if new_aranan is not None:
                aranan_json.aranan = new_aranan
            if new_degisken is not None:
                aranan_json.degisken = new_degisken
            if new_proje_id is not None:
                aranan_json.proje_id = new_proje_id
            self.session.refresh(aranan_json)
            return aranan_json
        return None

    def delete_aranan_json(self, json_id):
        aranan_json = self.session.query(ArananJson).filter_by(id=json_id).first()
        if aranan_json:
            self.session.delete(aranan_json)
            return True
        return False
