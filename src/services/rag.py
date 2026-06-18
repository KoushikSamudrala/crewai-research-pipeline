from pathlib import Path
import shutil
from typing import List
from src.utils.config import settings


def ensure_dirs():
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.KNOWLEDGE_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.STORAGE_DIR).mkdir(parents=True, exist_ok=True)


def copy_pdfs_to_knowledge(paths: List[str]) -> List[str]:
    ensure_dirs()
    copied = []
    for p in paths:
        src = Path(p)
        if src.suffix.lower() == ".pdf" and src.exists():
            dst = Path(settings.KNOWLEDGE_DIR) / src.name
            shutil.copy2(src, dst)
            copied.append(src.name)
    return copied
