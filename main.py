
import schedule
import time

import threading
from models.OrtakBaglanti import session_scope
from reader.ElasticSearchReader import ElasticSearchReader
from reader.SshReader import sshReader
from repository.Proje import ProjeManager
from repository.ProjeSinifMetod import ProjeSinifMetodManager
from util import FlaskRun
from util.GitRepoManager import GitRepoManager
from util.JavaCodeAnalyzer import JavaCodeAnalyzer



class logQuality:

    def __init__(self):

        self.schedule_thread = threading.Thread(target=self.run_schedule)
        self.rest_thread = threading.Thread(target=self.run_rest)
        self.ssh_start_thread = threading.Thread(target=sshReader().start)
        self.run_git_repo_thread = threading.Thread(target=self.run_git_repo)

        schedule.every(3).minutes.do(sshReader().start)
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

    es_reader = ElasticSearchReader()
    es_reader.start()

    log_processor = logQuality()
    log_processor.schedule_thread.start()
    #log_processor.rest_thread.start()
    log_processor.ssh_start_thread.start()
    log_processor.run_git_repo_thread.start()

    log_processor.schedule_thread.join()
    #log_processor.rest_thread.join()
    log_processor.ssh_start_thread.join()
    log_processor.run_git_repo_thread.join()



