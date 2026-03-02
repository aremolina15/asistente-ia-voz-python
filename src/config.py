"""
Configuración de la aplicación FastAPI
"""
from typing import Optional
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Ignorar variables extra para no fallar en carga
    )

    # Información de la App
    app_name: str = "DevOps Voice Assistant"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Configuración de GCP
    gcp_project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-central1")
    google_application_credentials: Optional[str] = Field(
        default=None,
        validation_alias="GOOGLE_APPLICATION_CREDENTIALS",
    )

    # Configuración de API
    api_title: str = "DevOps Voice Assistant API"
    api_version: str = "v1"
    api_prefix: str = "/api/v1"

    # Configuración de seguridad
    allowed_origins: list = ["*"]  # Cambiar en producción
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Advertencia de seguridad si se usa la clave por defecto en producción
        if not self.debug and self.secret_key == "dev-secret-key-change-in-production":
            import warnings
            warnings.warn(
                "⚠️  ADVERTENCIA DE SEGURIDAD: Usando SECRET_KEY por defecto en modo producción. "
                "Por favor configura SECRET_KEY en tu archivo .env con un valor único y seguro.",
                UserWarning,
                stacklevel=2
            )

    # Configuración de logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Configuración de Voice (Google Cloud Speech-to-Text)
    speech_to_text_enabled: bool = True
    text_to_speech_enabled: bool = True
    voice_default_language_code: str = Field(default="es-CO", validation_alias="VOICE_DEFAULT_LANGUAGE_CODE")
    voice_tts_name: Optional[str] = Field(default=None, validation_alias="VOICE_TTS_NAME")
    voice_tts_gender: str = Field(default="FEMALE", validation_alias="VOICE_TTS_GENDER")
    voice_tts_speaking_rate: float = Field(default=1.0, validation_alias="VOICE_TTS_SPEAKING_RATE")
    voice_tts_pitch: float = Field(default=0.0, validation_alias="VOICE_TTS_PITCH")

    # Configuración de IA (VertexAI)
    # Modelos disponibles: gemini-2.0-flash, gemini-1.5-flash, gemini-1.0-pro, text-bison
    vertex_ai_model: str = os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash")
    vertex_ai_temperature: float = float(os.getenv("VERTEX_AI_TEMPERATURE", "0.7"))
    vertex_ai_max_tokens: int = int(os.getenv("VERTEX_AI_MAX_TOKENS", "1024"))

    # Configuración RAG
    rag_enabled: bool = Field(default=False, validation_alias="RAG_ENABLED")
    rag_top_k: int = Field(default=5, validation_alias="RAG_TOP_K")
    rag_collection_name: str = Field(default="devops_knowledge", validation_alias="RAG_COLLECTION_NAME")
    rag_db_path: str = Field(default="data/chroma", validation_alias="RAG_DB_PATH")
    rag_knowledge_dir: str = Field(default="data/knowledge", validation_alias="RAG_KNOWLEDGE_DIR")
    rag_chunk_size: int = Field(default=800, validation_alias="RAG_CHUNK_SIZE")
    rag_chunk_overlap: int = Field(default=120, validation_alias="RAG_CHUNK_OVERLAP")
    rag_embedding_model: str = Field(default="text-embedding-005", validation_alias="RAG_EMBEDDING_MODEL")
    rag_strict_mode: bool = Field(default=True, validation_alias="RAG_STRICT_MODE")
    rag_min_lexical_overlap: float = Field(default=0.30, validation_alias="RAG_MIN_LEXICAL_OVERLAP")
    rag_vector_weight: float = Field(default=0.20, validation_alias="RAG_VECTOR_WEIGHT")
    rag_lexical_weight: float = Field(default=0.80, validation_alias="RAG_LEXICAL_WEIGHT")

    # Configuración de almacenamiento
    storage_bucket: str = os.getenv("STORAGE_BUCKET", "devops-assistant-storage")

    # Configuración de base de datos
    database_url: Optional[str] = os.getenv("DATABASE_URL", None)

    # Configuración de caché
    redis_url: Optional[str] = os.getenv("REDIS_URL", None)
    cache_ttl: int = 3600  # 1 hora


settings = Settings()
