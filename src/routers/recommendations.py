"""
Router para recomendaciones de DevOps
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from src.services.gcp_service import get_gcp_service

logger = logging.getLogger(__name__)
router = APIRouter()


class RecommendationRequest(BaseModel):
    """Solicitud de recomendaciones"""
    topic: str  # security, performance, cost, scalability, reliability
    context: str
    infrastructure: str = "gcp"  # gcp, kubernetes, terraform, etc


class Recommendation(BaseModel):
    """Modelo de recomendación"""
    title: str
    description: str
    priority: str  # low, medium, high, critical
    impact: str  # estimate of impact
    implementation_steps: List[str]


@router.post("/devops")
async def get_devops_recommendations(request: RecommendationRequest):
    """
    Obtener recomendaciones de DevOps
    
    Tópicos soportados:
    - security: Recomendaciones de seguridad
    - performance: Optimización de rendimiento
    - cost: Optimización de costos
    - scalability: Escalabilidad
    - reliability: Confiabilidad
    """
    try:
        gcp_service = get_gcp_service()
        
        prompt = f"""
        Como experto en DevOps, proporciona recomendaciones específicas para:
        
        Tópico: {request.topic}
        Contexto: {request.context}
        Infraestructura: {request.infrastructure}
        
        Proporciona al menos 3 recomendaciones detalladas en formato JSON con:
        - title: Título de la recomendación
        - description: Descripción detallada
        - priority: Nivel de prioridad (low/medium/high/critical)
        - impact: Impacto estimado
        - implementation_steps: Lista de pasos de implementación
        
        Responde SOLO con JSON válido.
        """
        
        response_text = gcp_service.get_ai_recommendation(prompt)
        
        # Parsear respuesta
        import json
        try:
            recommendations = json.loads(response_text)
            if isinstance(recommendations, dict) and "recommendations" in recommendations:
                recommendations = recommendations["recommendations"]
        except json.JSONDecodeError:
            recommendations = {
                "message": response_text,
                "note": "Respuesta no estructurada"
            }
        
        return {
            "topic": request.topic,
            "infrastructure": request.infrastructure,
            "recommendations": recommendations,
        }
    except Exception as e:
        logger.error(f"Error al obtener recomendaciones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick/{topic}")
async def get_quick_recommendations(topic: str):
    """
    Obtener recomendaciones rápidas por tópico
    
    Tópicos: security, performance, cost, scalability, reliability
    """
    try:
        quick_recommendations = {
            "security": [
                "Habilitar Cloud Audit Logs en todos los proyectos",
                "Usar Cloud KMS para gestión de claves",
                "Implementar VPC Service Controls",
                "Usar Private Google Access",
                "Habilitar Cloud Security Command Center",
            ],
            "performance": [
                "Usar Cloud CDN para distribuir contenido",
                "Implementar caching en Cloud Memorystore",
                "Optimizar tamaño de instancias",
                "Usar Cloud Load Balancing",
                "Implementar auto-scaling",
            ],
            "cost": [
                "Usar Committed Use Discounts (CUDs)",
                "Implementar Cloud Billing Alerts",
                "Usar Preemptible VMs para cargas no críticas",
                "Configurar automatic scaling",
                "Eliminar recursos no utilizados",
            ],
            "scalability": [
                "Usar Kubernetes autoscaling",
                "Implementar load balancing",
                "Usar Cloud Run para cargas serverless",
                "Configurar database sharding",
                "Usar Cloud Pub/Sub para mensajería",
            ],
            "reliability": [
                "Implementar multi-región deployment",
                "Usar Cloud Backup",
                "Configurar health checks",
                "Implementar disaster recovery",
                "Usar Cloud Monitoring y alertas",
            ],
        }
        
        recommendations = quick_recommendations.get(topic.lower(), [])
        
        if not recommendations:
            raise HTTPException(
                status_code=400,
                detail=f"Tópico no reconocido: {topic}"
            )
        
        return {
            "topic": topic,
            "recommendations": recommendations,
            "count": len(recommendations),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en recomendaciones rápidas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/infrastructure-assessment")
async def infrastructure_assessment(infrastructure_config: dict):
    """
    Evaluar configuración de infraestructura completa
    """
    try:
        gcp_service = get_gcp_service()
        
        prompt = f"""
        Evalúa la siguiente configuración de infraestructura y proporciona un assessment:
        
        {str(infrastructure_config)}
        
        Proporciona:
        1. Puntuación general (0-100)
        2. Áreas fortalecidas
        3. Áreas de mejora
        4. Recomendaciones prioritarias (top 5)
        5. Riesgos identificados
        
        Responde en formato JSON estructurado.
        """
        
        response_text = gcp_service.get_ai_recommendation(prompt)
        
        import json
        try:
            assessment = json.loads(response_text)
        except json.JSONDecodeError:
            assessment = {"assessment": response_text}
        
        return {
            "assessment": assessment,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error en infrastructure assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
