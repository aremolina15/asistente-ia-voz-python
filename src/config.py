"""
Configuración de la aplicación FastAPI
"""
from typing import Optional
import os

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

    # Configuración de IA (VertexAI)
    # Modelos disponibles: gemini-2.0-flash, gemini-1.5-flash, gemini-1.0-pro, text-bison
    vertex_ai_model: str = os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash")
    vertex_ai_temperature: float = float(os.getenv("VERTEX_AI_TEMPERATURE", "0.7"))
    vertex_ai_max_tokens: int = int(os.getenv("VERTEX_AI_MAX_TOKENS", "1024"))

    # Configuración de almacenamiento
    storage_bucket: str = os.getenv("STORAGE_BUCKET", "devops-assistant-storage")

    # Configuración de base de datos
    database_url: Optional[str] = os.getenv("DATABASE_URL", None)

    # Configuración de caché
    redis_url: Optional[str] = os.getenv("REDIS_URL", None)
    cache_ttl: int = 3600  # 1 hora


settings = Settings()
