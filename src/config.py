"""
Configuración de la aplicación FastAPI
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
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
    
    # Configuración de logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Configuración de Voice (Google Cloud Speech-to-Text)
    speech_to_text_enabled: bool = True
    text_to_speech_enabled: bool = True
    
    # Configuración de IA (VertexAI)
    vertex_ai_model: str = "gemini-1.5-pro"
    vertex_ai_temperature: float = 0.7
    vertex_ai_max_tokens: int = 1024
    
    # Configuración de almacenamiento
    storage_bucket: str = os.getenv("STORAGE_BUCKET", "devops-assistant-storage")
    
    # Configuración de base de datos
    database_url: Optional[str] = os.getenv("DATABASE_URL", None)
    
    # Configuración de caché
    redis_url: Optional[str] = os.getenv("REDIS_URL", None)
    cache_ttl: int = 3600  # 1 hora
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
