"""Catálogo de prompts versionables del proyecto."""

from .system_prompts import DEVOPS_SYSTEM_PROMPT
from .governance_prompts import build_governance_analysis_prompt
from .recommendation_prompts import (
    build_devops_recommendations_prompt,
    build_infrastructure_assessment_prompt,
)
from .rag_prompts import RAG_SYSTEM_PROMPT, build_rag_user_prompt

__all__ = [
    "DEVOPS_SYSTEM_PROMPT",
    "build_governance_analysis_prompt",
    "build_devops_recommendations_prompt",
    "build_infrastructure_assessment_prompt",
    "RAG_SYSTEM_PROMPT",
    "build_rag_user_prompt",
]
