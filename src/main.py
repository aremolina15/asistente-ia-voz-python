"""
Punto de entrada de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import settings
from src.routers import health, voice, governance, recommendations

# Configurar logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan de la aplicación
    """
    # Startup
    logger.info(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    logger.info(f"GCP Project: {settings.gcp_project_id}")
    yield
    # Shutdown
    logger.info("🛑 Cerrando aplicación")


# Crear instancia de FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.app_version,
    description="Asistente de IA con voz para DevOps enfocado en gobernanza y buenas prácticas",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(voice.router, prefix=f"{settings.api_prefix}/voice", tags=["Voice"])
app.include_router(
    governance.router, prefix=f"{settings.api_prefix}/governance", tags=["Governance"]
)
app.include_router(
    recommendations.router,
    prefix=f"{settings.api_prefix}/recommendations",
    tags=["Recommendations"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "api_prefix": settings.api_prefix,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
