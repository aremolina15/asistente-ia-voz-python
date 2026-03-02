"""Módulo RAG para recuperación de conocimiento DevOps."""

from .pipeline import RagPipeline

__all__ = ["RagPipeline", "run_ingest"]


def __getattr__(name: str):
	if name == "run_ingest":
		from .ingest import run_ingest

		return run_ingest
	raise AttributeError(name)
