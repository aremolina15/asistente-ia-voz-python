# Estándares CI/CD 2026

## Pipeline Obligatorio

1. Lint
2. Test unitarios
3. Test de seguridad (SAST)
4. Validación Terraform (plan)
5. Validación de costos (BigQuery Guardian)
6. Deploy controlado

## Reglas

- No usar secrets hardcoded
- Usar OIDC en GitHub → GCP
- No usar llaves JSON estáticas
- Terraform con backend remoto
- Uso de entornos separados: qa, st, prod

## Bloqueo automático si:

- score governance > 80
- IAM excesivo detectado
- SP sin límite de consumo