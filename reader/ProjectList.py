class project:
    @staticmethod
    def list():
        with session_scope() as session:
            proje = ProjeManager()
            projeler = proje.get_all_proje_sayac(session)
            proje.generate_short_hash_id()

            logger.info("Proje listesi çekildi")