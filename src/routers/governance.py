"""
Router para análisis de gobernanza
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from src.services.governance_service import GovernanceService

logger = logging.getLogger(__name__)
router = APIRouter()


class GovernanceAnalysisRequest(BaseModel):
    """Solicitud de análisis de gobernanza"""
    resource_type: str  # iam, storage, gke, compute
    resource_data: Dict[str, Any]
    include_recommendations: bool = True


class GovernanceAnalysisResponse(BaseModel):
    """Respuesta de análisis de gobernanza"""
    resource_type: str
    risk_level: str
    findings: list
    compliance_score: int
    recommendations: Optional[list] = None


@router.post("/analyze", response_model=GovernanceAnalysisResponse)
async def analyze_governance(request: GovernanceAnalysisRequest):
    """
    Analizar gobernanza de un recurso
    
    Tipos de recursos soportados:
    - iam: Análisis de políticas IAM
    - storage: Análisis de Cloud Storage
    - gke: Análisis de GKE
    - compute: Análisis de Compute Engine
    """
    try:
        resource_type = request.resource_type.lower()
        
        if resource_type == "iam":
            analysis = GovernanceService.analyze_iam_governance(request.resource_data)
        elif resource_type == "storage":
            analysis = GovernanceService.analyze_storage_governance(request.resource_data)
        elif resource_type == "gke":
            analysis = GovernanceService.analyze_gke_governance(request.resource_data)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de recurso no soportado: {resource_type}"
            )
        
        response = GovernanceAnalysisResponse(**analysis)
        
        if request.include_recommendations:
            response.recommendations = GovernanceService.get_best_practices_recommendations(
                resource_type
            )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis de gobernanza: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/best-practices/{resource_type}")
async def get_best_practices(resource_type: str):
    """
    Obtener recomendaciones de buenas prácticas
    
    Tipos soportados: iam, storage, gke, compute
    """
    try:
        resource_type = resource_type.lower()
        
        recommendations = GovernanceService.get_best_practices_recommendations(resource_type)
        
        if not recommendations:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de recurso no soportado: {resource_type}"
            )
        
        return {
            "resource_type": resource_type,
            "practices": recommendations,
            "total": len(recommendations),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener buenas prácticas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compliance-report")
async def generate_compliance_report(resources: Dict[str, Dict[str, Any]]):
    """
    Generar reporte de cumplimiento para múltiples recursos
    
    Ejemplo:
    {
        "iam": {...},
        "storage": {...},
        "gke": {...}
    }
    """
    try:
        report = {
            "total_resources": len(resources),
            "analyses": [],
            "overall_compliance_score": 0,
            "overall_risk_level": "bajo",
        }
        
        total_score = 0
        risk_levels = []
        
        for resource_type, resource_data in resources.items():
            if resource_type.lower() == "iam":
                analysis = GovernanceService.analyze_iam_governance(resource_data)
            elif resource_type.lower() == "storage":
                analysis = GovernanceService.analyze_storage_governance(resource_data)
            elif resource_type.lower() == "gke":
                analysis = GovernanceService.analyze_gke_governance(resource_data)
            else:
                continue
            
            report["analyses"].append(analysis)
            total_score += analysis["compliance_score"]
            risk_levels.append(analysis["risk_level"])
        
        if report["analyses"]:
            report["overall_compliance_score"] = int(total_score / len(report["analyses"]))
            # Determinar nivel de riesgo general
            if "crítico" in risk_levels:
                report["overall_risk_level"] = "crítico"
            elif "alto" in risk_levels:
                report["overall_risk_level"] = "alto"
            elif "medio" in risk_levels:
                report["overall_risk_level"] = "medio"
            else:
                report["overall_risk_level"] = "bajo"
        
        return report
    except Exception as e:
        logger.error(f"Error al generar reporte: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
