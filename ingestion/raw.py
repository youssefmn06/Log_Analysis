import gzip
import os
import zipfile
from logger import logger

def read_log_files(data_dir: str = "./data"):
    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        logger.error(f"Le dossier {data_dir} n'existe pas.")
        return

    # On récupère tous les fichiers (sans filtre strict sur l'extension finale)
    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    log_files = sorted([f for f in files if os.path.isfile(f)])

    logger.info(f"{len(log_files)} fichier(s) trouvé(s) dans {data_dir}")

    for file_path in log_files:
        logger.info(f"Lecture de : {os.path.basename(file_path)}")
        try:
            # 1. Essai de lecture en GZIP (pour auth.log.3, auth.log.4, *.gz)
            try:
                with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        yield line.strip()
                continue
            except Exception:
                pass

            # 2. Essai de lecture en ZIP (si un fichier .zip est présent)
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, "r") as z:
                    for name in z.namelist():
                        with z.open(name) as f:
                            for line in f:
                                yield line.decode("utf-8", errors="ignore").strip()
                continue

            # 3. Sinon, lecture en texte brut (pour auth.log, auth.log.1, etc.)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    yield line.strip()

        except Exception as e:
            logger.error(f"Erreur lors de la lecture de {file_path}: {e}")