import logging

from sentence_transformers import SentenceTransformer
from coderag.config.settings import *
from coderag.utils.common import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, model_path: str | None = None):
        path = model_path or EMBEDDING_MODEL_PATH
        logger.info("Loading embedding model from: %s", path)
        self.model = SentenceTransformer(path)

    def get_embedding(self, text: str):
        """
        Get embedding vector for a single text input
        """
        logger.debug("Encoding single text: %s...", text[:50])
        return self.model.encode(text, convert_to_numpy=True)

    def get_embeddings(self, texts: list[str]):
        """
        Get embedding vectors for multiple texts
        """
        logger.debug("Encoding %d texts", len(texts))
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.get_embeddings(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.get_embedding(text).tolist()