from abc import ABC, abstractmethod
from typing import List

class BaseDataProvider(ABC):
    """Abstract base class for providing file lists and content from a project source."""
    @abstractmethod
    def list_files(self) -> List[str]:
        """Return a list of all relevant file paths in the project."""
        pass
    @abstractmethod
    def get_file_content(self, file_path: str) -> str:
        """Return the content of a specific file."""
        pass