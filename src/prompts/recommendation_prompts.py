"""Prompts para recomendaciones DevOps e infraestructura."""


def build_devops_recommendations_prompt(topic: str, context: str, infrastructure: str) -> str:
    return f"""
Actúa como DevOps Senior en entorno bancario regulado con foco en GCP, Terraform, GitHub Actions y gobierno de costos.

Genera recomendaciones técnicas accionables para:

Topico: {topic}
Contexto: {context}
Infraestructura: {infrastructure}

Las recomendaciones deben:
- Priorizar seguridad IAM, principio de menor privilegio y control de costos.
- Considerar CI/CD empresarial y automatización.
- Incluir riesgos si no se implementa la recomendación.
- Ser viables en entorno GCP productivo.

Responde SOLO con JSON válido bajo el siguiente schema exacto:

{{
  "recommendations": [
    {{
      "title": "string",
      "description": "string",
      "priority": "low | medium | high | critical",
      "impact": "string",
      "risk_if_not_implemented": "string",
      "effort": "low | medium | high",
      "implementation_steps": [
        "string",
        "string",
        "string"
      ]
    }}
  ]
}}

Mínimo 3 recomendaciones.
No incluyas texto fuera del JSON.
""".strip()

def build_infrastructure_assessment_prompt(infrastructure_config: dict) -> str:
    return f"""
Actúa como arquitecto Cloud y DevOps Senior en entorno financiero regulado sobre GCP.

Evalúa la siguiente configuración:

{str(infrastructure_config)}

El assessment debe considerar:
- Seguridad IAM y service accounts
- Segmentación de ambientes
- Buenas prácticas Terraform
- Observabilidad y monitoreo
- Control de costos y límites en BigQuery
- Resiliencia y escalabilidad

Responde SOLO con JSON válido bajo el siguiente schema exacto:

{{
  "overall_score": 0,
  "security_score": 0,
  "cost_governance_score": 0,
  "ci_cd_maturity_score": 0,
  "strengths": ["string"],
  "improvement_areas": ["string"],
  "top_recommendations": [
    {{
      "title": "string",
      "priority": "low | medium | high | critical",
      "justification": "string"
    }}
  ],
  "identified_risks": [
    {{
      "risk": "string",
      "severity": "low | medium | high | critical",
      "mitigation": "string"
    }}
  ]
}}

No incluyas texto fuera del JSON.
""".strip()