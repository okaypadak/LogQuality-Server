from models.ArananRegexModel import ArananRegex

class ArananRegexManager:
    def __init__(self, session):
        self.session = session

    def create_regex_deger(self, aranan, degisken, proje_id):
        new_regex_deger = ArananRegex(aranan=aranan, degisken=degisken, proje_id=proje_id)
        self.session.add(new_regex_deger)
        self.session.commit()
        self.session.refresh(new_regex_deger)
        return new_regex_deger

    def read_regex_deger(self, regex_id):
        return self.session.query(ArananRegex).filter_by(id=regex_id).first()

    def update_regex_deger(self, regex_id, new_deger=None, new_proje_id=None):
        regex_deger = self.session.query(ArananRegex).filter_by(id=regex_id).first()
        if regex_deger:
            if new_deger is not None:
                regex_deger.deger = new_deger
            if new_proje_id is not None:
                regex_deger.proje_id = new_proje_id
            self.session.commit()
            self.session.refresh(regex_deger)
            return regex_deger
        return None

    def delete_regex_deger(self, regex_id):
        regex_deger = self.session.query(ArananRegex).filter_by(id=regex_id).first()
        if regex_deger:
            self.session.delete(regex_deger)
            self.session.commit()
            return True
        return False