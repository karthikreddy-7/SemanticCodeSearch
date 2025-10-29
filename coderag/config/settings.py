import os
from pathlib import Path

# Root path
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Embedding & Reranking models
# -------------------------------
EMBEDDING_MODEL_PATH = os.getenv(
    "EMBEDDING_MODEL_PATH",
    str(BASE_DIR / "models" / "all-MiniLM-L6-v2")
)

RERANKER_MODEL_PATH = os.getenv(
    "RERANKER_MODEL_PATH",
    str(BASE_DIR / "models" / "bge-reranker-base")
)

# -------------------------------
# Database settings
# -------------------------------
SQLITE_DB_PATH = os.getenv(
    "SQLITE_DB_PATH",
    str(BASE_DIR / "data" / "coderag.db")
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    str(BASE_DIR / "data" / "coderag.db")
)

# -------------------------------
# Data sources
# -------------------------------
DEFAULT_LOADER = os.getenv("DEFAULT_LOADER", "local")

# -------------------------------
# Auth tokens
# -------------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")

# -------------------------------
# Logging
# -------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
