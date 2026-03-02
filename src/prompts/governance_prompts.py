"""Prompts para análisis de gobernanza avanzado en entorno GCP empresarial."""

import json
from typing import Any, Dict


def build_governance_analysis_prompt(resource_type: str, resource_data: Dict[str, Any]) -> str:
    return f"""
Actúa como experto en Cloud Governance y DevOps en entorno financiero regulado sobre GCP.

Analiza la gobernanza del recurso tipo: {resource_type}

Datos del recurso:
{json.dumps(resource_data, indent=2)}

Evalúa específicamente:
- Seguridad IAM y principio de menor privilegio
- Uso de service accounts y permisos excesivos
- Segmentación por ambientes (qa, st, pr)
- Control de costos y límites de consumo
- Buenas prácticas Terraform e infraestructura como código
- Exposición pública o configuraciones inseguras
- Cumplimiento de CI/CD seguro

Responde SOLO con JSON válido bajo el siguiente schema exacto:

{{
  "overall_risk_level": "low | medium | high | critical",
  "security_issues": [
    {{
      "issue": "string",
      "severity": "low | medium | high | critical",
      "evidence": "string"
    }}
  ],
  "cost_governance_issues": [
    {{
      "issue": "string",
      "severity": "low | medium | high | critical",
      "potential_impact": "string"
    }}
  ],
  "devops_compliance": {{
    "ci_cd_alignment": "compliant | partially_compliant | non_compliant",
    "iac_alignment": "compliant | partially_compliant | non_compliant",
    "observability_alignment": "compliant | partially_compliant | non_compliant"
  }},
  "improvement_recommendations": [
    {{
      "title": "string",
      "priority": "low | medium | high | critical",
      "implementation_guidance": "string"
    }}
  ]
}}

No incluyas texto fuera del JSON.
""".strip()