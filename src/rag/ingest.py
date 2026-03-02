"""Ingesta de documentos para índice vectorial local (Chroma)."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from src.config import settings


SUPPORTED_EXTENSIONS = {".md", ".txt", ".rst", ".yaml", ".yml", ".tf", ".log", ".pdf"}


def _read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(pages)

    return path.read_text(encoding="utf-8", errors="ignore")


def _is_section_boundary(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True

    patterns = [
        r"^#{1,6}\s+",  # Markdown headings
        r"^(resource|module|variable|output|provider|terraform|data)\s+\"",  # Terraform blocks
        r"^[A-Za-z0-9_.-]+:\s*$",  # YAML key lines
        r"^---$",  # YAML separator
    ]
    return any(re.match(pattern, stripped, flags=re.IGNORECASE) for pattern in patterns)


def _split_structured_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    buffer: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")

        if _is_section_boundary(line) and buffer:
            block = "\n".join(buffer).strip()
            if block:
                blocks.append(block)
            buffer = []

        if line.strip():
            buffer.append(line)

    if buffer:
        block = "\n".join(buffer).strip()
        if block:
            blocks.append(block)

    return blocks


def _chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    blocks = _split_structured_blocks(text)
    if not blocks:
        return []

    chunks: list[str] = []
    current_words: list[str] = []

    max_words = max(80, chunk_size)
    overlap_words = max(0, min(chunk_overlap, max_words - 1))

    for block in blocks:
        block_words = block.split()

        if not block_words:
            continue

        if len(current_words) + len(block_words) <= max_words:
            current_words.extend(block_words)
            continue

        if current_words:
            chunks.append(" ".join(current_words).strip())
            current_words = current_words[-overlap_words:] if overlap_words else []

        if len(block_words) <= max_words:
            current_words.extend(block_words)
            continue

        step = max(1, max_words - overlap_words)
        index = 0
        while index < len(block_words):
            piece = " ".join(block_words[index:index + max_words]).strip()
            if piece:
                chunks.append(piece)
            index += step

    if current_words:
        chunks.append(" ".join(current_words).strip())

    return [chunk for chunk in chunks if chunk]


def run_ingest(data_dir: str = "data/knowledge") -> dict[str, Any]:
    import chromadb
    from vertexai.language_models import TextEmbeddingModel
    import vertexai

    base_dir = Path(data_dir)
    if not base_dir.exists():
        return {"indexed_chunks": 0, "files": 0, "message": f"Directorio no encontrado: {data_dir}"}

    vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)
    embedding_model = TextEmbeddingModel.from_pretrained(settings.rag_embedding_model)

    client = chromadb.PersistentClient(path=settings.rag_db_path)
    collection = client.get_or_create_collection(name=settings.rag_collection_name)

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, str]] = []

    indexed_files = 0
    for path in base_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        content = _read_text(path)
        chunks = _chunk_text(content, settings.rag_chunk_size, settings.rag_chunk_overlap)
        if not chunks:
            continue

        indexed_files += 1
        for index, chunk in enumerate(chunks):
            ids.append(f"{path.as_posix()}::{index}")
            documents.append(chunk)
            metadatas.append(
                {
                    "source": path.as_posix(),
                    "filename": path.name,
                    "extension": path.suffix.lower(),
                    "chunk_index": str(index),
                }
            )

    if not documents:
        return {"indexed_chunks": 0, "files": indexed_files, "message": "No se encontraron chunks para indexar"}

    embeddings = [item.values for item in embedding_model.get_embeddings(documents)]
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    return {"indexed_chunks": len(documents), "files": indexed_files, "collection": settings.rag_collection_name}


if __name__ == "__main__":
    result = run_ingest()
    print(result)
