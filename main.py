import schedule
import time
import threading
import logging
from models.OrtakBaglanti import session_scope
from reader.ElasticSearchReader import ElasticSearchReader
from repository.Proje import ProjeManager
from repository.ProjeSinifMetod import ProjeSinifMetodManager
from util import FlaskRun
from util.GitRepoManager import GitRepoManager
from util.JavaCodeAnalyzer import JavaCodeAnalyzer

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        # logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

class logQuality:

    def __init__(self):
        self.schedule_thread = threading.Thread(target=self.run_schedule)
        self.rest_thread = threading.Thread(target=self.run_rest)
        self.run_git_repo_thread = threading.Thread(target=self.run_git_repo)

        schedule.every(3).minutes.do(self.run_git_repo)

    def run_schedule(self):
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            logger.error("Error in run_schedule: %s", e, exc_info=True)

    def run_rest(self):
        try:
            FlaskRun.app.run()
        except Exception as e:
            logger.error("Error in run_rest: %s", e, exc_info=True)

    def run_git_repo(self):
        try:
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
        except Exception as e:
            logger.error("Error in run_git_repo: %s", e, exc_info=True)

if __name__ == "__main__":
    try:
        es_reader = ElasticSearchReader()
        es_reader.start()

        log_processor = logQuality()
        log_processor.schedule_thread.start()
        #log_processor.rest_thread.start()
        #log_processor.run_git_repo_thread.start()

        log_processor.schedule_thread.join()
        #log_processor.rest_thread.join()
        #log_processor.run_git_repo_thread.join()
    except Exception as e:
        logger.error("Error in main: %s", e, exc_info=True)
