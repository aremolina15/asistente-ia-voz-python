"""
Tests para el servicio de gobernanza
"""
import pytest
from src.services.governance_service import GovernanceService, RiskLevel


def test_analyze_iam_governance_critical_issues():
    """Test análisis de IAM con problemas críticos"""
    iam_data = {
        "service_accounts": list(range(15)),  # Demasiadas
        "bindings": {
            "user@example.com": list(range(10))  # Demasiados roles
        },
        "uses_custom_roles": False,
        "audit_logging_enabled": False,
    }
    
    result = GovernanceService.analyze_iam_governance(iam_data)
    
    assert result["resource_type"] == "iam"
    assert result["risk_level"] in [RiskLevel.HIGH, RiskLevel.CRITICAL]
    assert len(result["findings"]) > 0
    assert result["compliance_score"] < 100


def test_analyze_storage_governance_public_bucket():
    """Test análisis de Storage con bucket público"""
    storage_data = {
        "encryption_enabled": True,
        "versioning_enabled": True,
        "lifecycle_policy": {"rules": []},
        "is_public": True,  # Problema crítico
        "audit_logging_enabled": True,
    }
    
    result = GovernanceService.analyze_storage_governance(storage_data)
    
    assert result["resource_type"] == "storage"
    assert result["risk_level"] == RiskLevel.CRITICAL
    assert any("público" in str(f).lower() for f in result["findings"])


def test_analyze_gke_governance_secure():
    """Test análisis de GKE seguro"""
    gke_data = {
        "rbac_enabled": True,
        "network_policy_enabled": True,
        "pod_security_policy_enabled": True,
        "resource_quotas_configured": True,
        "audit_logging_enabled": True,
    }
    
    result = GovernanceService.analyze_gke_governance(gke_data)
    
    assert result["resource_type"] == "gke"
    assert result["risk_level"] == RiskLevel.LOW
    assert len(result["findings"]) == 0


def test_get_best_practices():
    """Test obtener recomendaciones de buenas prácticas"""
    practices = GovernanceService.get_best_practices_recommendations("iam")
    
    assert len(practices) > 0
    assert all("practice" in p and "description" in p for p in practices)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
