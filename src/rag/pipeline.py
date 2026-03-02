"""Pipeline RAG para recuperación + generación asistida por contexto."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from src.config import settings
from src.prompts.rag_prompts import RAG_SYSTEM_PROMPT, build_rag_user_prompt
from src.services.gcp_service import get_gcp_service


class RagPipeline:
    def __init__(self):
        import chromadb
        import vertexai
        from vertexai.language_models import TextEmbeddingModel

        vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)

        self.embedding_model = TextEmbeddingModel.from_pretrained(settings.rag_embedding_model)
        self.client = chromadb.PersistentClient(path=settings.rag_db_path)
        self.collection = self.client.get_or_create_collection(name=settings.rag_collection_name)

    @staticmethod
    def _normalize_text(value: str) -> str:
        normalized = unicodedata.normalize("NFD", value.lower())
        normalized = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
        return normalized

    def _extract_terms(self, question: str) -> list[str]:
        normalized = self._normalize_text(question)
        terms = re.findall(r"[a-z0-9_./-]{3,}", normalized)

        stopwords = {
            "para", "como", "donde", "cuando", "porque", "sobre", "entre", "desde", "hasta",
            "esta", "este", "estos", "estas", "que", "con", "sin", "una", "uno", "unos", "unas",
            "por", "del", "las", "los", "el", "la", "y", "o", "de", "en", "se", "es", "un", "al",
        }
        unique_terms: list[str] = []
        seen: set[str] = set()
        for term in terms:
            if term in stopwords or term in seen:
                continue
            seen.add(term)
            unique_terms.append(term)

        return unique_terms[:12]

    def _lexical_overlap_score(self, query_terms: list[str], document: str) -> float:
        if not query_terms:
            return 0.0

        normalized_doc = self._normalize_text(document)
        doc_terms = set(re.findall(r"[a-z0-9_./-]{3,}", normalized_doc))
        if not doc_terms:
            return 0.0

        overlap = sum(1 for term in query_terms if term in doc_terms)
        return overlap / max(len(query_terms), 1)

    def _matched_terms_count(self, query_terms: list[str], document: str) -> int:
        if not query_terms:
            return 0

        normalized_doc = self._normalize_text(document)
        doc_terms = set(re.findall(r"[a-z0-9_./-]{3,}", normalized_doc))
        return sum(1 for term in query_terms if term in doc_terms)

    def retrieve(self, question: str, top_k: int | None = None) -> dict[str, Any]:
        k = top_k or settings.rag_top_k
        candidate_k = max(k * 4, 16)
        query_terms = self._extract_terms(question)
        query_embedding = self.embedding_model.get_embeddings([question])[0].values

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=candidate_k,
            include=["documents", "metadatas", "distances"],
        )

        candidates: dict[str, dict[str, Any]] = {}

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]

        for index, doc_id in enumerate(ids):
            document = documents[index] if index < len(documents) else ""
            metadata = metadatas[index] if index < len(metadatas) else {}
            distance = distances[index] if index < len(distances) else 2.0

            vector_score = 1.0 / (1.0 + max(distance, 0.0))
            lexical_score = self._lexical_overlap_score(query_terms, document)
            matched_terms = self._matched_terms_count(query_terms, document)

            if settings.rag_strict_mode and query_terms and lexical_score < settings.rag_min_lexical_overlap:
                continue

            score = (settings.rag_vector_weight * vector_score) + (settings.rag_lexical_weight * lexical_score)

            candidates[doc_id] = {
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "score": score,
                "lexical_score": lexical_score,
                "matched_terms": matched_terms,
                "source": metadata.get("source", "unknown"),
            }

        for term in query_terms[:8]:
            try:
                term_result = self.collection.get(
                    where_document={"$contains": term},
                    limit=min(candidate_k, 12),
                    include=["documents", "metadatas"],
                )
            except Exception:
                continue

            term_ids = term_result.get("ids", [])
            term_documents = term_result.get("documents", [])
            term_metadatas = term_result.get("metadatas", [])

            for index, doc_id in enumerate(term_ids):
                document = term_documents[index] if index < len(term_documents) else ""
                metadata = term_metadatas[index] if index < len(term_metadatas) else {}
                lexical_score = self._lexical_overlap_score(query_terms, document)
                matched_terms = self._matched_terms_count(query_terms, document)
                bonus = 0.15

                if settings.rag_strict_mode and query_terms and lexical_score < settings.rag_min_lexical_overlap:
                    continue

                if doc_id in candidates:
                    candidates[doc_id]["score"] += bonus
                    candidates[doc_id]["score"] += 0.25 * lexical_score
                    candidates[doc_id]["lexical_score"] = max(
                        candidates[doc_id].get("lexical_score", 0.0), lexical_score
                    )
                    candidates[doc_id]["matched_terms"] = max(
                        candidates[doc_id].get("matched_terms", 0), matched_terms
                    )
                else:
                    candidates[doc_id] = {
                        "id": doc_id,
                        "document": document,
                        "metadata": metadata,
                        "score": 0.35 + (0.65 * lexical_score),
                        "lexical_score": lexical_score,
                        "matched_terms": matched_terms,
                        "source": metadata.get("source", "unknown"),
                    }

        ranked = sorted(
            candidates.values(),
            key=lambda item: (
                item.get("score", 0.0),
                item.get("lexical_score", 0.0),
                item.get("matched_terms", 0),
            ),
            reverse=True,
        )[:k]

        contexts = [item["document"] for item in ranked if item["document"]]

        sources: list[str] = []
        for item in ranked:
            source = item.get("source", "unknown")
            if source not in sources:
                sources.append(source)

        return {
            "contexts": contexts,
            "sources": sources,
        }

    def answer(self, question: str) -> dict[str, Any]:
        retrieval = self.retrieve(question)
        contexts = retrieval["contexts"]
        sources = retrieval["sources"]

        rag_prompt = build_rag_user_prompt(question, contexts)
        gcp_service = get_gcp_service()
        response = gcp_service.get_ai_recommendation(
            rag_prompt,
            system_instruction=RAG_SYSTEM_PROMPT,
        )

        return {
            "response": response,
            "sources": sources,
            "contexts_count": len(contexts),
        }
