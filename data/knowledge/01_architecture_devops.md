# Arquitectura DevOps – Asistente Inteligente en GCP

## Principios

1. Infraestructura como Código (IaC)
2. Seguridad Zero-Trust
3. Gobernanza Activa
4. Observabilidad First
5. FinOps Integrado
6. Automatización Total

## Arquitectura por Capas

Cliente → API (FastAPI) → Servicios GCP → RAG → Gobernanza → Observabilidad

### Componentes

- Cloud Run (backend principal)
- Vertex AI (LLM + embeddings)
- Cloud Storage (artefactos y RAG)
- BigQuery (análisis y gobernanza)
- GitHub Actions (CI/CD)
- Terraform (Infraestructura)
- Secret Manager
- Cloud Logging + Trace

## Reglas 2026

- No se despliega sin validación de políticas.
- Todo PR debe pasar por análisis automatizado.
- Toda consulta BigQuery debe tener límite de consumo.
- Todo servicio debe tener health y readiness.
- Todo entorno debe tener SA dedicada.