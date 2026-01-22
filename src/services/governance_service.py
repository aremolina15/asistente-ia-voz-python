"""
Servicio de análisis de gobernanza
"""
import logging
from typing import Dict, Any, List
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(str, Enum):
    """Niveles de riesgo"""
    LOW = "bajo"
    MEDIUM = "medio"
    HIGH = "alto"
    CRITICAL = "crítico"


class GovernanceService:
    """Servicio para análisis de gobernanza"""

    # Reglas de gobernanza
    GOVERNANCE_RULES = {
        "iam": {
            "max_service_accounts_per_project": 10,
            "max_roles_per_principal": 5,
            "should_use_custom_roles": True,
            "should_have_audit_logging": True,
            "should_implement_least_privilege": True,
        },
        "storage": {
            "should_have_encryption": True,
            "should_have_versioning": True,
            "should_have_lifecycle_policy": True,
            "should_be_private": True,
            "should_have_audit_logging": True,
        },
        "compute": {
            "should_use_managed_images": True,
            "should_have_monitoring": True,
            "should_have_labels": True,
            "should_use_preemptible_for_dev": True,
            "should_have_startup_shutdown_scripts": True,
        },
        "gke": {
            "should_have_rbac_enabled": True,
            "should_have_network_policy": True,
            "should_have_pod_security_policy": True,
            "should_have_resource_quotas": True,
            "should_enable_audit_logging": True,
            "should_use_authorized_networks": True,
        },
    }

    @staticmethod
    def analyze_iam_governance(iam_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar gobernanza de IAM
        
        Args:
            iam_data: Datos de IAM
            
        Returns:
            Análisis de gobernanza
        """
        findings = []
        risk_level = RiskLevel.LOW

        # Verificar número de cuentas de servicio
        service_accounts = iam_data.get("service_accounts", [])
        if len(service_accounts) > GovernanceService.GOVERNANCE_RULES["iam"]["max_service_accounts_per_project"]:
            findings.append({
                "severity": "medium",
                "issue": "Demasiadas cuentas de servicio",
                "recommendation": f"Reducir cuentas de servicio a {GovernanceService.GOVERNANCE_RULES['iam']['max_service_accounts_per_project']} o menos",
                "count": len(service_accounts),
            })
            risk_level = RiskLevel.MEDIUM

        # Verificar permisos excesivos
        excessive_permissions = []
        for principal, roles in iam_data.get("bindings", {}).items():
            if len(roles) > GovernanceService.GOVERNANCE_RULES["iam"]["max_roles_per_principal"]:
                excessive_permissions.append({
                    "principal": principal,
                    "role_count": len(roles),
                    "roles": roles,
                })

        if excessive_permissions:
            findings.append({
                "severity": "high",
                "issue": "Permisos excesivos detectados",
                "recommendation": "Implementar principio de menor privilegio",
                "principals": excessive_permissions,
            })
            risk_level = RiskLevel.HIGH

        # Verificar uso de roles personalizados
        if not iam_data.get("uses_custom_roles", False):
            findings.append({
                "severity": "low",
                "issue": "No se utilizan roles personalizados",
                "recommendation": "Considerar crear roles personalizados para casos de uso específicos",
            })

        # Verificar logging de auditoría
        if not iam_data.get("audit_logging_enabled", False):
            findings.append({
                "severity": "high",
                "issue": "Logging de auditoría no habilitado",
                "recommendation": "Habilitar Cloud Audit Logs para IAM",
            })
            risk_level = RiskLevel.HIGH

        return {
            "resource_type": "iam",
            "risk_level": risk_level,
            "findings": findings,
            "compliance_score": 100 - (len(findings) * 10),
        }

    @staticmethod
    def analyze_storage_governance(storage_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar gobernanza de Cloud Storage
        
        Args:
            storage_data: Datos de storage
            
        Returns:
            Análisis de gobernanza
        """
        findings = []
        risk_level = RiskLevel.LOW

        # Verificar encriptación
        if not storage_data.get("encryption_enabled", False):
            findings.append({
                "severity": "critical",
                "issue": "Encriptación no habilitada",
                "recommendation": "Habilitar encriptación en el bucket de storage",
            })
            risk_level = RiskLevel.CRITICAL

        # Verificar versionado
        if not storage_data.get("versioning_enabled", False):
            findings.append({
                "severity": "medium",
                "issue": "Versionado no habilitado",
                "recommendation": "Habilitar versionado para recuperación de datos",
            })

        # Verificar políticas de ciclo de vida
        if not storage_data.get("lifecycle_policy", None):
            findings.append({
                "severity": "medium",
                "issue": "Política de ciclo de vida no configurada",
                "recommendation": "Configurar política de ciclo de vida para optimizar costos",
            })

        # Verificar acceso público
        if storage_data.get("is_public", False):
            findings.append({
                "severity": "critical",
                "issue": "Bucket público detectado",
                "recommendation": "Cambiar permisos a privado inmediatamente",
            })
            risk_level = RiskLevel.CRITICAL

        # Verificar logging
        if not storage_data.get("audit_logging_enabled", False):
            findings.append({
                "severity": "high",
                "issue": "Logging de acceso no habilitado",
                "recommendation": "Habilitar logging para auditoría de acceso",
            })
            risk_level = max(risk_level, RiskLevel.HIGH)

        return {
            "resource_type": "storage",
            "risk_level": risk_level,
            "findings": findings,
            "compliance_score": max(0, 100 - (len(findings) * 15)),
        }

    @staticmethod
    def analyze_gke_governance(gke_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar gobernanza de GKE
        
        Args:
            gke_data: Datos de GKE
            
        Returns:
            Análisis de gobernanza
        """
        findings = []
        risk_level = RiskLevel.LOW

        # Verificar RBAC
        if not gke_data.get("rbac_enabled", False):
            findings.append({
                "severity": "critical",
                "issue": "RBAC no habilitado",
                "recommendation": "Habilitar RBAC en el cluster de GKE",
            })
            risk_level = RiskLevel.CRITICAL

        # Verificar Network Policy
        if not gke_data.get("network_policy_enabled", False):
            findings.append({
                "severity": "high",
                "issue": "Network Policy no habilitada",
                "recommendation": "Habilitar Network Policy para segmentación de red",
            })
            risk_level = max(risk_level, RiskLevel.HIGH)

        # Verificar Pod Security Policy
        if not gke_data.get("pod_security_policy_enabled", False):
            findings.append({
                "severity": "high",
                "issue": "Pod Security Policy no habilitada",
                "recommendation": "Habilitar Pod Security Policy o Pod Security Standards",
            })
            risk_level = max(risk_level, RiskLevel.HIGH)

        # Verificar Resource Quotas
        if not gke_data.get("resource_quotas_configured", False):
            findings.append({
                "severity": "medium",
                "issue": "Resource Quotas no configuradas",
                "recommendation": "Configurar resource quotas por namespace",
            })

        # Verificar Audit Logging
        if not gke_data.get("audit_logging_enabled", False):
            findings.append({
                "severity": "high",
                "issue": "Audit Logging no habilitado",
                "recommendation": "Habilitar auditoría de cluster",
            })
            risk_level = max(risk_level, RiskLevel.HIGH)

        return {
            "resource_type": "gke",
            "risk_level": risk_level,
            "findings": findings,
            "compliance_score": max(0, 100 - (len(findings) * 12)),
        }

    @staticmethod
    def get_best_practices_recommendations(resource_type: str) -> List[Dict[str, str]]:
        """
        Obtener recomendaciones de buenas prácticas
        
        Args:
            resource_type: Tipo de recurso
            
        Returns:
            Lista de recomendaciones
        """
        recommendations = {
            "iam": [
                {
                    "practice": "Principio de menor privilegio",
                    "description": "Otorgar solo los permisos mínimos necesarios",
                },
                {
                    "practice": "Separación de responsabilidades",
                    "description": "Usar roles personalizados para separar funciones",
                },
                {
                    "practice": "Auditoría regular",
                    "description": "Revisar permisos mensualmente",
                },
            ],
            "storage": [
                {
                    "practice": "Encriptación en reposo",
                    "description": "Usar Customer-Managed Encryption Keys (CMEK)",
                },
                {
                    "practice": "Versionado y backup",
                    "description": "Habilitar versionado y backup automático",
                },
                {
                    "practice": "Control de acceso",
                    "description": "Usar políticas de acceso basadas en identidad",
                },
            ],
            "gke": [
                {
                    "practice": "Seguridad en capas",
                    "description": "Implementar RBAC, Network Policy, PSP",
                },
                {
                    "practice": "Monitoreo continuo",
                    "description": "Usar Cloud Monitoring y Security Command Center",
                },
                {
                    "practice": "Actualizaciones de seguridad",
                    "description": "Mantener cluster y nodos actualizados",
                },
            ],
        }

        return recommendations.get(resource_type, [])
