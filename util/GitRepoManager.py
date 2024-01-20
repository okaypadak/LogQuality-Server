import subprocess
import os
import util.LogProcess as log

class GitRepoManager:

    def __init__(self):
        self.base_path = "c:\\git"

    def clone_or_pull_repo(self, repo_url):
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(self.base_path, repo_name)

        if os.path.exists(repo_path):
            log.logger.info(f"{repo_path} dizini zaten var. Pull yapılıyor...")
            result = subprocess.run(['git', 'pull'], cwd=repo_path, capture_output=True, text=True)

            if "Already up to date" in result.stdout:
                log.logger.info(f"{repo_path} dizini zaten güncel.")
                update = False
            else:
                log.logger.info(result.stdout)
                log.logger.error(result.stderr)
                update = True
        else:
            log.logger.info(f"{repo_path} dizini bulunamadı. Klonlama yapılıyor...")
            subprocess.run(['git', 'clone', repo_url, repo_path])
            update = True

        return update, repo_path

    def fetch_and_pull_if_needed(self, repo_url):
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(self.base_path, repo_name)

        log.logger.info(f"Fetching changes for {repo_path}...")
        subprocess.run(['git', 'fetch'], cwd=repo_path)

        # İlgili branch'in son durumunu al
        current_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_path, text=True).strip()

        # Uzak depodaki son durumu al
        remote_commit = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=repo_path, text=True).strip()

        if current_commit != remote_commit:
            log.logger.info("Yeni commit bulundu. Pull yapılıyor...")
            subprocess.run(['git', 'pull'], cwd=repo_path)
            log.logger.info("Pull işlemi tamamlandı.")
        else:
            log.logger.info("Yeni commit bulunamadı. Güncelleme yapılmıyor.")
