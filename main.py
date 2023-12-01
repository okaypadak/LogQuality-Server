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
from repository.Proje import ProjeManager



def read_remote_log_file(gelen):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(gelen['sunucu_ip'], username=gelen['kullanici_adi'], password=gelen['kullanici_sifre'])
        sftp = ssh_client.open_sftp()

        with sftp.file(gelen['log_dosya_yolu'], 'r') as dosya:
            dosya.seek(gelen['gunluk_sayac'])
            lines = dosya.readlines()
            new_position = dosya.tell()

        return gelen['proje_id'], lines, gelen['gunluk_sayac_id'], new_position

    except Exception as e:
        print(f"Hata: {e}")
        return None

    finally:
        sftp.close()
        ssh_client.close()


def process_log_files(proje_listesi):
    with ThreadPoolExecutor() as executor:
        # list comprehension
        futures = {executor.submit(read_remote_log_file, proje): proje for proje in proje_listesi}

        for future in concurrent.futures.as_completed(futures):
            proje_id, lines, sayac_id, new_position = future.result()

            #gunluk_sayac güncelle

            if lines is not None:
                for line in lines:
                    satir_ayristir(line)
                print(f"New Position for {proje_id}: {new_position}")

            else:
                print(f"Error reading remote log file for {proje_id}.")


def satir_ayristir(satir):
    




def get_regex_values(desen, metin):
    eslesmeler = re.findall(desen, metin)
    return eslesmeler


def test_proje_create():
    # session = SessionScope()
    with session_scope() as session:
        proje_instance = ProjeManager.create_proje(session, "Proje 1", "192.168.1.1", 22 , "admin", "1234", "/var/log/Apache",1)



def get_json_values(json_str, variable_name):
    try:

        data = json.loads(json_str)

        value = data.get(variable_name)

        if value is not None:
            return value
        else:
            return f"{variable_name} bulunamadı."

    except json.JSONDecodeError as e:
        return f"Hata: JSON çözümlenemedi. {e}"


def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError:
        return False


def proje_listesi():
    with session_scope() as session:

        proje = ProjeManager()
        projeler = proje.get_all_proje_sayac(session)

    process_log_files(projeler)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_rest():
    rest.app.run()


if __name__ == "__main__":
    schedule.every(1).minutes.do(proje_listesi)

    schedule_thread = threading.Thread(target=run_schedule)
    rest_thread = threading.Thread(target=run_rest)
    proje_listesi_thread = threading.Thread(target=proje_listesi)

    # Start both threads
    schedule_thread.start()
    #rest_thread.start()
    proje_listesi_thread.start()

    # Wait for both threads to finish
    schedule_thread.join()
    #rest_thread.join()
    proje_listesi_thread.join()