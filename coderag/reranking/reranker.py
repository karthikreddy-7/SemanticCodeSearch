import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from coderag.config.settings import RERANKER_MODEL_PATH
from coderag.utils.common import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class Reranker:
    """
    reranker using a cross-encoder style model.
    """
    def __init__(self, model_path: str | None = None, device: str | None = None):
        path = model_path or RERANKER_MODEL_PATH
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        logger.info("Loading reranker model from: %s", path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.model.to(self.device)
        self.model.eval()

    def score(self, query: str, document: str) -> float:
        """
        Compute a relevance score between a query and a single document.
        """
        logger.debug("Scoring query-doc pair: '%s' vs '%s'", query[:40], document[:40])
        inputs = self.tokenizer(
            query,
            document,
            return_tensors="pt",
            truncation=True,
            padding=True,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            score = outputs.logits.squeeze().item()

        return float(score)

    def rerank(self, query: str, documents: list[str]) -> list[tuple[str, float]]:
        """
        Rerank a list of documents by relevance to the given query.
        Returns a sorted list of (document, score) tuples.
        """
        logger.info("Reranking %d documents for query: '%s'", len(documents), query)
        results = [(doc, self.score(query, doc)) for doc in documents]
        results.sort(key=lambda x: x[1], reverse=True)
        return results
