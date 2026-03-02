"""
Punto de entrada de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from src.routers import health, voice, governance, recommendations

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración básica
APP_NAME = "DevOps Voice Assistant"
APP_VERSION = "1.0.0"
API_PREFIX = "/api/v1"

try:
    from src.config import settings
    GCP_PROJECT = settings.gcp_project_id
except:
    GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "not-configured")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan de la aplicación
    """
    # Startup
    logger.info(f"🚀 Iniciando {APP_NAME} v{APP_VERSION}")
    logger.info(f"GCP Project: {GCP_PROJECT}")
    yield
    # Shutdown
    logger.info("🛑 Cerrando aplicación")


# Crear instancia de FastAPI
app = FastAPI(
    title="DevOps Voice Assistant API",
    version=APP_VERSION,
    description="Asistente de IA con voz para DevOps enfocado en gobernanza y buenas prácticas",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(voice.router, prefix=f"{API_PREFIX}/voice", tags=["voice"])
app.include_router(governance.router, prefix=f"{API_PREFIX}/governance", tags=["governance"])
app.include_router(recommendations.router, prefix=f"{API_PREFIX}/recommendations", tags=["recommendations"])
app.include_router(health.router, tags=["health"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
        "api_prefix": API_PREFIX,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
