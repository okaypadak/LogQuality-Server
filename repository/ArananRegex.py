from models.ArananRegexModel import ArananRegex

class ArananRegexManager:

    def create_regex_deger(self, session, aranan, degisken, proje_id):
        new_regex_deger = ArananRegex(aranan=aranan, degisken=degisken, proje_id=proje_id)
        session.add(new_regex_deger)
        session.commit()
        session.refresh(new_regex_deger)
        return new_regex_deger

    def get_all_regex(self, session):
        return session.query(ArananRegex).all()

    @staticmethod
    def get_regexes_by_aranan_id(session, aranan_id):
        regexler = session.query(ArananRegex).filter_by(aranan_id=aranan_id).all()

        grouped_regex = {}
        for item in regexler:
            grouped_regex[item.degisken] = item.deger

        return grouped_regex

    def read_regex_deger(self, session, regex_id):
        return session.query(ArananRegex).filter_by(id=regex_id).first()

    def update_regex_deger(self, session, regex_id, new_deger=None, new_proje_id=None):
        regex_deger = session.query(ArananRegex).filter_by(id=regex_id).first()
        if regex_deger:
            if new_deger is not None:
                regex_deger.deger = new_deger
            if new_proje_id is not None:
                regex_deger.proje_id = new_proje_id
            session.refresh(regex_deger)
            return regex_deger
        return None

    def delete_regex_deger(self, session, regex_id):
        regex_deger = session.query(ArananRegex).filter_by(id=regex_id).first()
        if regex_deger:
            session.delete(regex_deger)
            return True
        return False