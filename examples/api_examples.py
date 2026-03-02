#!/usr/bin/env python3
"""
Ejemplos de uso de la API del Asistente DevOps Voice
"""

import requests
import json
from typing import Dict, Any

# URL base de la API (ajustar según ambiente)
BASE_URL = "http://localhost:8000/api/v1"


class DevOpsAssistantClient:
    """Cliente para interactuar con el asistente DevOps"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def analyze_governance(
        self,
        resource_type: str,
        resource_data: Dict[str, Any],
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """
        Analizar gobernanza de un recurso
        
        Args:
            resource_type: iam, storage, gke, compute
            resource_data: Datos del recurso
            include_recommendations: Incluir recomendaciones
            
        Returns:
            Análisis de gobernanza
        """
        payload = {
            "resource_type": resource_type,
            "resource_data": resource_data,
            "include_recommendations": include_recommendations
        }
        
        response = self.session.post(
            f"{self.base_url}/governance/analyze",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_best_practices(self, resource_type: str) -> Dict[str, Any]:
        """Obtener buenas prácticas para un recurso"""
        response = self.session.get(
            f"{self.base_url}/governance/best-practices/{resource_type}"
        )
        response.raise_for_status()
        return response.json()
    
    def get_devops_recommendations(
        self,
        topic: str,
        context: str,
        infrastructure: str = "gcp"
    ) -> Dict[str, Any]:
        """
        Obtener recomendaciones de DevOps
        
        Args:
            topic: security, performance, cost, scalability, reliability
            context: Contexto de la consulta
            infrastructure: gcp, kubernetes, terraform
        """
        payload = {
            "topic": topic,
            "context": context,
            "infrastructure": infrastructure
        }
        
        response = self.session.post(
            f"{self.base_url}/recommendations/devops",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_quick_recommendations(self, topic: str) -> Dict[str, Any]:
        """Obtener recomendaciones rápidas"""
        response = self.session.get(
            f"{self.base_url}/recommendations/quick/{topic}"
        )
        response.raise_for_status()
        return response.json()


def example_1_iam_analysis():
    """Ejemplo 1: Analizar gobernanza de IAM"""
    print("\n" + "="*60)
    print("📋 EJEMPLO 1: Análisis de Gobernanza IAM")
    print("="*60)
    
    client = DevOpsAssistantClient()
    
    # Datos de ejemplo con problemas
    iam_config = {
        "service_accounts": list(range(12)),  # Demasiadas (máx 10)
        "bindings": {
            "admin@example.com": ["Editor", "Owner", "Viewer", "Storage.Admin"],  # Demasiados roles
            "dev@example.com": ["Viewer"],
        },
        "uses_custom_roles": False,
        "audit_logging_enabled": False,  # Crítico
    }
    
    try:
        result = client.analyze_governance(
            resource_type="iam",
            resource_data=iam_config,
            include_recommendations=True
        )
        
        print(f"\n✅ Tipo de Recurso: {result['resource_type']}")
        print(f"🚨 Nivel de Riesgo: {result['risk_level']}")
        print(f"📊 Puntuación de Cumplimiento: {result['compliance_score']}/100")
        print(f"\n🔍 Hallazgos ({len(result['findings'])} encontrados):")
        
        for i, finding in enumerate(result['findings'], 1):
            print(f"\n   {i}. [{finding.get('severity', 'INFO').upper()}] {finding.get('issue', 'N/A')}")
            print(f"      Recomendación: {finding.get('recommendation', 'N/A')}")
        
        if result.get('recommendations'):
            print(f"\n💡 Buenas Prácticas:")
            for practice in result['recommendations'][:3]:
                print(f"   • {practice['practice']}: {practice['description']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_2_storage_analysis():
    """Ejemplo 2: Analizar gobernanza de Storage"""
    print("\n" + "="*60)
    print("📦 EJEMPLO 2: Análisis de Gobernanza Cloud Storage")
    print("="*60)
    
    client = DevOpsAssistantClient()
    
    storage_config = {
        "encryption_enabled": True,
        "versioning_enabled": False,  # Problema
        "lifecycle_policy": None,  # Problema
        "is_public": False,
        "audit_logging_enabled": True,
    }
    
    try:
        result = client.analyze_governance(
            resource_type="storage",
            resource_data=storage_config
        )
        
        print(f"\n✅ Tipo de Recurso: {result['resource_type']}")
        print(f"🚨 Nivel de Riesgo: {result['risk_level']}")
        print(f"📊 Puntuación: {result['compliance_score']}/100")
        print(f"\n⚠️ Problemas encontrados: {len(result['findings'])}")
        
        for finding in result['findings']:
            print(f"   • {finding['issue']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_3_quick_recommendations():
    """Ejemplo 3: Obtener recomendaciones rápidas"""
    print("\n" + "="*60)
    print("⚡ EJEMPLO 3: Recomendaciones Rápidas de Seguridad")
    print("="*60)
    
    client = DevOpsAssistantClient()
    
    try:
        result = client.get_quick_recommendations("security")
        
        print(f"\n🔒 Recomendaciones de {result['topic'].upper()}:")
        print(f"Total: {result['count']} recomendaciones\n")
        
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"{i}. {rec}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_4_devops_recommendations():
    """Ejemplo 4: Obtener recomendaciones DevOps avanzadas"""
    print("\n" + "="*60)
    print("🚀 EJEMPLO 4: Recomendaciones DevOps Avanzadas")
    print("="*60)
    
    client = DevOpsAssistantClient()
    
    try:
        result = client.get_devops_recommendations(
            topic="scalability",
            context="Tenemos 5 instancias de GKE con aplicaciones basadas en microservicios",
            infrastructure="gcp"
        )
        
        print(f"\n📈 Recomendaciones para: {result['topic']}")
        print(f"Infraestructura: {result['infrastructure']}\n")
        
        recommendations = result.get('recommendations', [])
        if isinstance(recommendations, list):
            for i, rec in enumerate(recommendations[:3], 1):
                if isinstance(rec, str):
                    print(f"{i}. {rec}")
                else:
                    print(f"{i}. {rec.get('title', 'N/A')}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_5_gke_best_practices():
    """Ejemplo 5: Buenas prácticas para GKE"""
    print("\n" + "="*60)
    print("☸️  EJEMPLO 5: Buenas Prácticas para GKE")
    print("="*60)
    
    client = DevOpsAssistantClient()
    
    try:
        result = client.get_best_practices("gke")
        
        print(f"\n💡 Prácticas para {result['resource_type'].upper()}:")
        print(f"Total: {result['total']} prácticas\n")
        
        for i, practice in enumerate(result['practices'], 1):
            print(f"{i}. {practice['practice']}")
            print(f"   → {practice['description']}\n")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def print_header():
    """Imprimir encabezado"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " EJEMPLOS DE USO - DevOps Voice Assistant API ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    print("\n📌 Nota: Asegúrate de que la API esté ejecutándose en http://localhost:8000")


def main():
    """Ejecutar todos los ejemplos"""
    print_header()
    
    try:
        # Verificar conexión
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Conexión a API: OK (Status: {response.status_code})\n")
    except:
        print("❌ No se puede conectar a la API")
        print("   Ejecuta primero: python -m uvicorn src.main:app --reload")
        return
    
    # Ejecutar ejemplos
    try:
        example_1_iam_analysis()
        example_2_storage_analysis()
        example_3_quick_recommendations()
        example_4_devops_recommendations()
        example_5_gke_best_practices()
    except Exception as e:
        print(f"\n❌ Error durante ejecución: {str(e)}")
    
    print("\n" + "="*60)
    print("✨ Ejemplos completados!")
    print("="*60)
    print("\n📚 Más información:")
    print("   • Documentación API: http://localhost:8000/docs")
    print("   • README: Ver README.md")
    print("   • Arquitectura: Ver ARCHITECTURE.md")


if __name__ == "__main__":
    main()
