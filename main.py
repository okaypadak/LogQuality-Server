import concurrent
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import paramiko
import schedule
import time
import re
import rest
import threading
from ortakbaglanti import session_scope
from repository.ArananRegex import ArananRegexManager
from repository.GunlukSayac import GunlukSayacManager
from repository.Proje import ProjeManager
from repository.Takip import TakipManager


class LogProcessor:

    def __init__(self):
        self.schedule_thread = threading.Thread(target=self.run_schedule)
        self.rest_thread = threading.Thread(target=self.run_rest)
        self.proje_listesi_thread = threading.Thread(target=self.proje_listesi)

        schedule.every(3).minutes.do(self.proje_listesi)

    def read_remote_log_file(self, gelen):

        global sftp

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
            print(f"Hata: {e}")
            return None

        finally:
            try:
                if sftp:
                    sftp.close()
                if ssh_client:
                    ssh_client.close()
            except Exception as e:
                print(f"Hata: {e}")

    def tum_eslesmeler(self, satirlar, proje_id):

        takipManager = TakipManager()

        text = "\n".join(satirlar)
        pattern = re.compile(r"(?m)^.*?Exception.*(?:\n+^\s*at .*)+", re.MULTILINE)
        matches = pattern.finditer(text)
        match_list = [match.group() for match in matches]

        for match in match_list:
            pattern = re.compile(r"\b\w+\.\w+\.+\w+Exception\b", re.MULTILINE)
            exceptions = pattern.findall(match)
            print(f"Yakalanan kelime: {exceptions}")

            for exception in exceptions:
                with session_scope() as session:
                    takipManager.create_or_update_takip(session, exception, proje_id)





    def get_regex_values(self, desen, satir):
        eslesmeler = re.findall(desen, satir)
        return eslesmeler

    def get_json_values(self, json_str, variable_name):
        try:
            data = json.loads(json_str)
            value = data.get(variable_name)

            if value is not None:
                return value
            else:
                return f"{variable_name} bulunamadı."

        except json.JSONDecodeError as e:
            return f"Hata: JSON çözümlenemedi. {e}"

    def satir_ayristir(self, satirlar, proje_id):
        arananRegexManager = ArananRegexManager()
        takipManager = TakipManager()

        tum_regex = arananRegexManager.get_regexes_by_proje_id(proje_id)

        if satirlar is not None:
            for satir in satirlar:
                gelen_hata = self.get_regex_values("java.*.Exception", satir)
                with session_scope() as session:
                    takipManager.create_or_update_takip(session, gelen_hata)

    def ayristir(self, proje_id, secim, satirlar):
        if secim == 1:
            self.tum_eslesmeler(satirlar, proje_id)
        elif secim == 2:
            self.satir_ayristir(satirlar, proje_id)

    def process_log_files(self, proje_listesi):
        with (ThreadPoolExecutor() as executor):
            # list comprehension
            futures = {executor.submit(self.read_remote_log_file, proje): proje for proje in proje_listesi}

            for future in concurrent.futures.as_completed(futures):
                proje_id, secim, lines, sayac_id, yeni_sira = future.result()

                gunlukSayacManager = GunlukSayacManager()

                with session_scope() as session:
                    gunlukSayacManager.update_gunluk_sayac(session, sayac_id, None, yeni_sira, None)

                self.ayristir(proje_id, secim, lines)

    def proje_listesi(self):
        with session_scope() as session:
            proje = ProjeManager()
            projeler = proje.get_all_proje_sayac(session)

        self.process_log_files(projeler)

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_rest(self):
        rest.app.run()


if __name__ == "__main__":
    log_processor = LogProcessor()

    # Start both threads
    log_processor.schedule_thread.start()
    # log_processor.rest_thread.start()
    log_processor.proje_listesi_thread.start()

    # Wait for both threads to finish
    log_processor.schedule_thread.join()
    # log_processor.rest_thread.join()
    log_processor.proje_listesi_thread.join()
