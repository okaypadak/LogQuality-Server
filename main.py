import concurrent
import json
from concurrent.futures import ThreadPoolExecutor
import paramiko
import schedule
import time
import re
import threading
from models.OrtakBaglanti import session_scope
from repository.ArananRegex import ArananRegexManager
from repository.GunlukSayac import GunlukSayacManager
from repository.Proje import ProjeManager
from repository.ProjeSinifMetod import ProjeSinifMetodManager
from repository.Takip import TakipManager
from util import FlaskRun
from util import LogProcess as log
from util.GitRepoManager import GitRepoManager
from util.JavaCodeAnalyzer import JavaCodeAnalyzer


class logsTrack:

    def __init__(self):

        reader = sshReader()

        self.schedule_thread = threading.Thread(target=self.run_schedule)
        self.rest_thread = threading.Thread(target=self.run_rest)
        self.proje_listesi_thread = threading.Thread(target=reader.proje_listesi)
        self.run_git_repo_thread = threading.Thread(target=self.run_git_repo)

        schedule.every(3).minutes.do(reader.proje_listesi)
        schedule.every(3).minutes.do(self.run_git_repo)


    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_rest(self):
        FlaskRun.app.run()

    def run_git_repo(self):

        gitRepoManager = GitRepoManager()

        with session_scope() as session:
            proje = ProjeManager()
            projeler = proje.get_all_projeler(session)

            for proje in projeler:
                update, repo_path = gitRepoManager.clone_or_pull_repo(proje.git_url)

                if update:
                    analyzer = JavaCodeAnalyzer(repo_path)
                    result = analyzer.analyze_project()
                    print(result)
                    with session_scope() as session:
                        projeSinifMetodManager = ProjeSinifMetodManager()
                        projeSinifMetodManager.create_list(session, result, proje.id)


if __name__ == "__main__":
    log_processor = logsTrack()

    # Start both threads
    log_processor.schedule_thread.start()
    log_processor.rest_thread.start()
    log_processor.proje_listesi_thread.start()
    log_processor.run_git_repo_thread.start()

    # Wait for both threads to finish
    log_processor.schedule_thread.join()
    log_processor.rest_thread.join()
    log_processor.proje_listesi_thread.join()
    log_processor.run_git_repo_thread.join()
