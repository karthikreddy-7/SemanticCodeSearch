# coderag/db/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional, Any

from coderag.database.relational.models import *
from coderag.database.relational.models import Repository, Chunk


# -------------------------------------------------------------------
# 🧱 REPOSITORY OPERATIONS
# -------------------------------------------------------------------

def get_repository_by_name(db: Session, name: str) -> Optional[Repository]:
    """Fetch repository by name."""
    return db.query(Repository).filter(Repository.name == name).first()


def create_repository(db: Session, name: str, path: str, hash: str) -> Repository:
    """Create a new repository entry."""
    repo = Repository(name=name, path=path, hash=hash)
    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo


def update_repository_hash(db: Session, repo: Repository, new_hash: str):
    """Update repository hash when repo content changes."""
    repo.hash = new_hash
    repo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(repo)
    return repo


def delete_repository(db: Session, repo: Repository):
    """Delete repository and cascade all related files & chunks."""
    db.delete(repo)
    db.commit()


def list_repositories(db: Session) -> list[type[Repository]]:
    """List all repositories."""
    return db.query(Repository).all()


# -------------------------------------------------------------------
# 📄 FILE OPERATIONS
# -------------------------------------------------------------------

def get_file(db: Session, repo_id: int, file_path: str) -> Optional[File]:
    """Fetch file by path within a repo."""
    return (
        db.query(File)
        .filter(File.repository_id == repo_id, File.path == file_path)
        .first()
    )


def create_file(
    db: Session,
    repo_id: int,
    name: str,
    path: str,
    hash: str,
    language: Optional[str] = None,
) -> File:
    """Create file if not exists; update hash if changed."""
    file = File(
        repository_id=repo_id,
        name=name,
        path=path,
        hash=hash,
        language=language,
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def delete_file(db: Session, file: File):
    """Delete a file and cascade all chunks."""
    db.delete(file)
    db.commit()


def list_files(db: Session, repo_id: int) -> list[type[File]]:
    """List all files in a repository."""
    return db.query(File).filter(File.repository_id == repo_id).all()


# -------------------------------------------------------------------
# 🧩 CHUNK OPERATIONS
# -------------------------------------------------------------------

def get_chunks_by_file(db: Session, file_id: int) -> list[type[Chunk]]:
    """Get all chunks belonging to a specific file."""
    return db.query(Chunk).filter(Chunk.file_id == file_id).all()


def get_chunk_by_hash(db: Session, file_id: int, chunk_hash: str) -> Optional[Chunk]:
    """Fetch chunk by hash (used to check existing embeddings)."""
    return (
        db.query(Chunk)
        .filter(Chunk.file_id == file_id, Chunk.hash == chunk_hash)
        .first()
    )


def create_chunk(
    db: Session,
    repository_id: int,
    file_id: int,
    chunk_type: str,
    name: str,
    signature: Optional[str],
    start_line: int,
    end_line: int,
    hash: str,
    embedding_id: Optional[str] = None,
) -> Chunk:
    """Insert a new chunk (class or method level)."""
    chunk = Chunk(
        repository_id=repository_id,
        file_id=file_id,
        chunk_type=chunk_type,
        name=name,
        signature=signature,
        start_line=start_line,
        end_line=end_line,
        hash=hash,
        embedding_id=embedding_id,
    )
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk


def delete_chunk(db: Session, chunk: Chunk):
    """Delete a single chunk."""
    db.delete(chunk)
    db.commit()


def delete_chunks_by_file(db: Session, file_id: int):
    """Bulk delete all chunks for a file."""
    db.query(Chunk).filter(Chunk.file_id == file_id).delete()
    db.commit()


def list_all_chunks(db: Session) -> list[type[Chunk]]:
    """List all chunks (for debugging or full sync)."""
    return db.query(Chunk).all()
