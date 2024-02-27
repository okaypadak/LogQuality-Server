class project:
    @staticmethod
    def list():
        with session_scope() as session:
            proje = ProjeManager()
            projeler = proje.get_all_proje_sayac(session)
            proje.generate_short_hash_id()

            log.logger.info("Proje listesi çekildi")

        sshReader.process_log_files(projeler)