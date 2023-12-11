import subprocess
import os
import LogProcess

def clone_or_pull_repo(repo_url, local_path):
    if os.path.exists(local_path):
        LogProcess.info(f"{local_path} dizini zaten var. Pull yapılıyor...")
        subprocess.run(['git', 'pull'], cwd=local_path)
    else:
        LogProcess.info(f"{local_path} dizini bulunamadı. Klonlama yapılıyor...")
        subprocess.run(['git', 'clone'], repo_url, local_path)

def fetch_and_pull_if_needed(repo_path):
    LogProcess.info(f"Fetching changes for {repo_path}...")
    subprocess.run(['git', 'fetch'], cwd=repo_path)

    # İlgili branch'in son durumunu al
    current_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_path, text=True).strip()

    # Uzak depodaki son durumu al
    remote_commit = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=repo_path, text=True).strip()

    if current_commit != remote_commit:
        LogProcess.info("Yeni commit bulundu. Pull yapılıyor...")
        subprocess.run(['git', 'pull'], cwd=repo_path)
        LogProcess.info("Pull işlemi tamamlandı.")
    else:
        LogProcess.info("Yeni commit bulunamadı. Güncelleme yapılmıyor.")