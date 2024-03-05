import paramiko
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from models.OrtakBaglanti import session_scope
from reader.ProjectList import project
from repository.ArananRegex import ArananRegexManager
from repository.GunlukSayac import GunlukSayacManager
from repository.Takip import TakipManager
from util.LogProcess import logger


class sshReader:

    def read_remote_log_file(self, gelen):
        sftp = None
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                gelen['sunucu_ip'], username=gelen['kullanici_adi'], password=gelen['kullanici_sifre']
            )
            sftp = ssh_client.open_sftp()

            with sftp.file(gelen['log_dosya_yolu'], 'r') as dosya:
                dosya.seek(gelen['sira'])
                lines = dosya.readlines()
                new_position = dosya.tell()

            return gelen['proje_id'], gelen['secim'], lines, gelen['gunluk_sayac_id'], new_position

        except Exception as e:
            logger.error(f"{gelen['proje_adi']} projesinde SSH bağlantısı sağlanamadı")

        finally:
            try:
                if sftp:
                    sftp.close()
                if ssh_client:
                    ssh_client.close()
            except Exception as e:
                logger.error(f"Hata: SSH Bağlantısı yapılmadı")

    def tumu(self, satirlar, proje_id):
        takipManager = TakipManager()

        text = "\n".join(satirlar)
        pattern = re.compile(r"(?m)^.*?Exception.*(?:\n+^\s*at .*)+", re.MULTILINE)
        matches = pattern.finditer(text)
        match_list = [match.group() for match in matches]

        for match in match_list:
            pattern = re.compile(r"\b\w+\.\w+\.+\w+Exception\b", re.MULTILINE)
            exceptions = pattern.findall(match)

            for exception in exceptions:
                with session_scope() as session:
                    takipManager.create_or_update_takip(session, exception, proje_id)

    def regex_values(self, desen, satir):
        eslesmeler = re.findall(desen, satir)
        return eslesmeler

    def satir(self, satirlar, proje_id):
        arananRegexManager = ArananRegexManager()
        takipManager = TakipManager()

        tum_regex = arananRegexManager.get_regexes_by_proje_id(proje_id)

        if satirlar is not None:
            for satir in satirlar:
                gelen_hata = self.regex_values("java.*.Exception", satir)
                with session_scope() as session:
                    takipManager.create_or_update_takip(session, gelen_hata)

    def ayristir(self, proje_id, secim, satirlar):
        if secim == 1:
            self.tumu(satirlar, proje_id)
        elif secim == 2:
            self.satir(satirlar, proje_id)

    def start(self):

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.read_remote_log_file, proje): proje for proje in project.list()}

            for future in as_completed(futures):
                try:
                    if future.result() is not None:

                        proje_id, secim, lines, sayac_id, yeni_sira = future.result()

                        if proje_id is not None:
                            gunlukSayacManager = GunlukSayacManager()

                            with session_scope() as session:
                                gunlukSayacManager.update_gunluk_sayac(session, sayac_id, None, yeni_sira, None)

                            self.ayristir(proje_id, secim, lines)

                except RuntimeError as e:
                    logger.error(f"Hata: Future doğru sonuç türetmedi")
