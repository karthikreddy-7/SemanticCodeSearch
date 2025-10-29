import logging
from typing import List
from coderag.config.settings import *
from coderag.data.base_loader import BaseDataProvider
from coderag.utils.common import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class LocalDataProvider(BaseDataProvider):
    """Provides data from a local filesystem path."""
    def __init__(self, project_path: str):
        if not os.path.isdir(project_path):
            raise ValueError(f"Path is not a valid directory: {project_path}")
        self.project_path = project_path
        logger.debug(f"Initialized LocalDataProvider for path: {project_path}")

    def list_files(self) -> List[str]:
        all_files = []
        for root, dirs, files in os.walk(self.project_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

            for file in files:
                if file not in IGNORED_FILES and os.path.splitext(file)[1] in ALLOWED_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.project_path)
                    all_files.append(rel_path)
                    logger.debug(f"Added file: {rel_path}")
                else:
                    logger.debug(f"Ignored file: {file}")
        logger.info(f"Total local files after filtering: {len(all_files)}")
        return all_files

    def get_file_content(self, file_path: str) -> str:
        full_path = os.path.join(self.project_path, file_path)
        logger.debug(f"Reading local file: {full_path}")
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        logger.debug(f"Read {len(content)} characters from file: {file_path}")
        return content