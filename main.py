#from takip import create_entry, read_all_entries, update_entry, delete_entry
import json
import logging

from paramiko import sftp as ssh
import schedule
import time
import re
import rest

import threading

def read_remote_log_file():

    konum = None

    ssh_client = ssh.SSHClient()
    ssh_client.set_missing_host_key_policy(ssh.AutoAddPolicy())

    # Sunucu bilgileri
    hostname = 'uzak_sunucu_ip_adresi'
    username = 'kullanici_adi'
    password = 'sifre'

    try:
        ssh_client.connect(hostname, username=username, password=password)
        sftp = ssh_client.open_sftp()

        remote_log_path = '/uzak/dizin/logdosyasi.log'

        with sftp.file(remote_log_path, 'r') as dosya:
            dosya.seek(0 if not konum else konum)
            for satir in dosya:
                print(satir)
                konum = dosya.tell()

    except Exception as e:
        print(f"Hata: {e}")

    finally:
        sftp.close()
        ssh_client.close()


def get_regex_values(desen, metin):

    eslesmeler = re.findall(desen, metin)
    return eslesmeler


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


def load_projects():

    return

def test():
    print("Test çalıştı")
    logging.info("Test çalıştı")


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_rest():
    rest.app.run()


if __name__ == "__main__":
    # create_entry('2023-11-12', 'example', 'GET', 'None')
    # update_entry(1, 'Updated error message')
    # read_all_entries()

    schedule.every(10).minutes.do(test)

    # Create threads for schedule and rest functions
    schedule_thread = threading.Thread(target=run_schedule)
    rest_thread = threading.Thread(target=run_rest)

    # Start both threads
    schedule_thread.start()
    rest_thread.start()

    # Wait for both threads to finish
    schedule_thread.join()
    rest_thread.join()