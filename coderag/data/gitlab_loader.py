import logging
import os
import gitlab
from typing import List, Optional
from urllib.parse import urlparse

from coderag.data.base_loader import BaseDataProvider
from coderag.config.settings import *
from coderag.utils.common import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class GitLabDataProvider(BaseDataProvider):
    """Provides data by fetching from a remote GitLab repository via API."""
    def __init__(self, repo_url: str, branch: Optional[str] = None, token: str = GITLAB_TOKEN):
        self.repo_url = repo_url
        logger.debug(f"Initializing GitLabDataProvider for repo: {repo_url}")
        self.gl = gitlab.Gitlab("https://gitlab.com", private_token=token)
        project_path = self._get_project_path(repo_url)
        logger.debug(f"Converted repo URL to project path: {project_path}")
        self.project = self.gl.projects.get(project_path)
        self.branch = branch or self.project.default_branch or "main"
        logger.info(f"Using branch: {self.branch}")

    def _get_project_path(self, repo_url: str) -> str:
        """Convert GitLab URL to project path (namespace/project_name)."""
        return urlparse(repo_url).path.strip("/")

    def list_files(self) -> List[str]:
        files = []
        items = self.project.repository_tree(ref=self.branch, recursive=True, all=True)
        logger.debug(f"Fetched {len(items)} items from GitLab repository tree")
        for item in items:
            path_parts = item["path"].split('/')
            file_name = path_parts[-1]

            if item["type"] == "blob":
                if any(part in IGNORED_FOLDERS for part in path_parts):
                    logger.debug(f"Ignored folder in path: {item['path']}")
                    continue
                if file_name in IGNORED_FILES:
                    logger.debug(f"Ignored file: {file_name}")
                    continue
                if os.path.splitext(file_name)[1] not in ALLOWED_EXTENSIONS:
                    logger.debug(f"Skipped file due to extension filter: {file_name}")
                    continue
                files.append(item["path"])
                logger.debug(f"Added file: {item['path']}")
        logger.info(f"Total files after filtering: {len(files)}")
        return files

    def get_file_content(self, file_path: str) -> str:
        logger.debug(f"Fetching content for file: {file_path}")
        f = self.project.files.get(file_path=file_path, ref=self.branch)
        content = f.decode().decode("utf-8")
        logger.debug(f"Fetched {len(content)} characters for file: {file_path}")
        return content