"""
Punto de entrada de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

from src.routers import voice

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
# NOTA: En producción, configura allowed_origins con dominios específicos
# Ejemplo: allowed_origins=["https://tudominio.com", "https://app.tudominio.com"]
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(voice.router, prefix=f"{API_PREFIX}/voice", tags=["voice"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
        "api_prefix": API_PREFIX,
    }



# ============================================================================
# HEALTH ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": APP_NAME,
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================================================
# GOVERNANCE ENDPOINTS
# ============================================================================

@app.post(f"{API_PREFIX}/governance/analyze")
async def analyze_governance(data: dict):
    """Analizar gobernanza de un recurso"""
    resource_type = data.get("resource_type", "unknown").lower()
    resource_data = data.get("resource_data", {})
    
    findings = []
    risk_level = "bajo"
    
    if resource_type == "iam":
        service_accounts = resource_data.get("service_accounts", [])
        if len(service_accounts) > 10:
            findings.append({
                "severity": "medium",
                "issue": "Demasiadas cuentas de servicio",
                "recommendation": "Reducir a máximo 10 cuentas"
            })
            risk_level = "medio"
            
        if not resource_data.get("audit_logging_enabled"):
            findings.append({
                "severity": "high",
                "issue": "Audit Logging no habilitado",
                "recommendation": "Habilitar Cloud Audit Logs"
            })
            risk_level = "alto"
    
    elif resource_type == "storage":
        if resource_data.get("is_public"):
            findings.append({
                "severity": "critical",
                "issue": "Bucket público",
                "recommendation": "Cambiar a privado inmediatamente"
            })
            risk_level = "crítico"
            
        if not resource_data.get("encryption_enabled"):
            findings.append({
                "severity": "high",
                "issue": "Encriptación no habilitada",
                "recommendation": "Habilitar encriptación"
            })
            risk_level = "alto"
    
    compliance_score = max(0, 100 - (len(findings) * 15))
    
    return {
        "resource_type": resource_type,
        "risk_level": risk_level,
        "findings": findings,
        "compliance_score": compliance_score,
        "recommendations": []
    }


@app.get(f"{API_PREFIX}/governance/best-practices/{{resource_type}}")
async def get_best_practices(resource_type: str):
    """Obtener buenas prácticas"""
    practices = {
        "iam": [
            {"practice": "Principio de menor privilegio", "description": "Otorgar solo permisos mínimos"},
            {"practice": "Separación de responsabilidades", "description": "Usar roles personalizados"},
            {"practice": "Auditoría regular", "description": "Revisar permisos mensualmente"}
        ],
        "storage": [
            {"practice": "Encriptación en reposo", "description": "Usar CMEK"},
            {"practice": "Versionado y backup", "description": "Habilitar versionado automático"},
            {"practice": "Control de acceso", "description": "Usar políticas basadas en identidad"}
        ],
        "gke": [
            {"practice": "Seguridad en capas", "description": "Implementar RBAC, Network Policy"},
            {"practice": "Monitoreo continuo", "description": "Usar Cloud Monitoring"},
            {"practice": "Actualizaciones", "description": "Mantener cluster actualizado"}
        ]
    }
    
    resource_type = resource_type.lower()
    practices_list = practices.get(resource_type, [])
    
    return {
        "resource_type": resource_type,
        "practices": practices_list,
        "total": len(practices_list)
    }


# ============================================================================
# RECOMMENDATIONS ENDPOINTS
# ============================================================================

@app.get(f"{API_PREFIX}/recommendations/quick/{{topic}}")
async def get_quick_recommendations(topic: str):
    """Obtener recomendaciones rápidas"""
    recommendations_by_topic = {
        "security": [
            "Habilitar Cloud Audit Logs",
            "Usar Cloud KMS para gestión de claves",
            "Implementar VPC Service Controls",
            "Usar Private Google Access",
            "Habilitar Cloud Security Command Center"
        ],
        "performance": [
            "Usar Cloud CDN",
            "Implementar caching en Memorystore",
            "Optimizar tamaño de instancias",
            "Usar Cloud Load Balancing",
            "Implementar auto-scaling"
        ],
        "cost": [
            "Usar Committed Use Discounts",
            "Implementar Billing Alerts",
            "Usar Preemptible VMs",
            "Configurar automatic scaling",
            "Eliminar recursos no utilizados"
        ],
        "scalability": [
            "Usar Kubernetes autoscaling",
            "Implementar load balancing",
            "Usar Cloud Run para serverless",
            "Configurar database sharding",
            "Usar Cloud Pub/Sub"
        ],
        "reliability": [
            "Implementar multi-región",
            "Usar Cloud Backup",
            "Configurar health checks",
            "Implementar disaster recovery",
            "Usar Cloud Monitoring y alertas"
        ]
    }
    
    topic = topic.lower()
    recommendations = recommendations_by_topic.get(topic, [])
    
    if not recommendations:
        return {"error": f"Tópico no reconocido: {topic}", "status": "error"}
    
    return {
        "topic": topic,
        "recommendations": recommendations,
        "count": len(recommendations)
    }


@app.post(f"{API_PREFIX}/recommendations/devops")
async def get_devops_recommendations(data: dict):
    """Obtener recomendaciones DevOps"""
    topic = data.get("topic", "general")
    context = data.get("context", "")
    
    return {
        "topic": topic,
        "context": context[:100] + "..." if len(context) > 100 else context,
        "recommendations": [
            "Revisar documentación relevante",
            "Implementar cambios en ambiente de staging",
            "Ejecutar tests completos",
            "Documentar cambios",
            "Comunicar con el equipo"
        ],
        "priority": "medium"
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
