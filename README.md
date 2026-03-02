# Asistente IA con Voz para DevOps

Un asistente inteligente con capacidades de voz que ayuda a profesionales DevOps a implementar buenas prácticas, gobernanza y infraestructura en la nube.

## 🎯 Características Principales

- **Consultas de Voz**: Interacción natural mediante reconocimiento de voz
- **Análisis de Gobernanza**: Evaluación de políticas y compliance
- **Recomendaciones de Buenas Prácticas**: Sugerencias basadas en infraestructura
- **Integración GCP**: Cloud Storage, Compute Engine, Kubernetes, IAM
- **Respuestas Inteligentes**: Powered by VertexAI/Gemini
- **Auditoría y Logs**: Registro completo de consultas y recomendaciones

## 🏗️ Arquitectura

### Vista rápida (para presentación)

```
┌───────────────────┐      ┌─────────────────────────────┐      ┌──────────────────────────┐
│ Cliente de Voz    │ ---> │ API FastAPI (src/main.py)   │ ---> │ Servicios GCP + VertexAI │
│ (voice_client.py) │      │ Routers + lógica de negocio │      │ STT, TTS, GenAI, Storage │
└───────────────────┘      └─────────────────────────────┘      └──────────────────────────┘
```

### Capas del sistema

- **Capa 1 – Interfaz**: Cliente de voz (`voice_client.py`) y consumo HTTP de la API.
- **Capa 2 – API**: FastAPI en `src/main.py`, que enruta requests a módulos especializados.
- **Capa 3 – Dominio**: Reglas DevOps/Gobernanza en `src/services/governance_service.py`.
- **Capa 4 – IA y Cloud**: Integración con GCP y Vertex AI en `src/services/gcp_service.py`.

### Flujo end-to-end

1. El usuario habla o envía consulta de texto.
2. `POST /api/v1/voice/transcribe` convierte audio a texto (Speech-to-Text).
3. `POST /api/v1/voice/query` construye la respuesta con Vertex AI (Gemini).
4. La respuesta puede sintetizarse con `POST /api/v1/voice/synthesize` (Text-to-Speech).
5. El sistema retorna JSON + audio (base64) y deja trazabilidad en logs.

### Mapeo interno de componentes

- **Orquestación de API**: `src/main.py`
- **Endpoints de voz**: `src/routers/voice.py`
- **Endpoints de gobernanza**: `src/routers/governance.py`
- **Endpoints de recomendaciones**: `src/routers/recommendations.py`
- **Health/Readiness**: `src/routers/health.py`
- **Servicios cloud/GenAI**: `src/services/gcp_service.py`
- **Motor de reglas DevOps**: `src/services/governance_service.py`

## 📋 Requisitos

- Python 3.10+
- GCP Project con credentials configuradas
- Docker y Docker Compose
- Kubernetes (opcional, para deployment)

## 🚀 Inicio Rápido

### 1. Configurar Entorno

```bash
# Clonar el repositorio
git clone https://github.com/aremolina15/asistente-ia-voz-python.git
cd asistente-ia-voz-python

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar GCP

```bash
# Autenticación con GCP
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT=your-project-id
```

### 3. Ejecutar la Aplicación

```bash
# Modo desarrollo
python -m uvicorn src.main:app --reload

# La API estará disponible en http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

## 📁 Estructura del Proyecto

```
asistente-ia-voz-python/
├── src/
│   ├── main.py                     # FastAPI app + registro de routers
│   ├── config.py                   # Configuración central
│   ├── routers/
│   │   ├── health.py               # Health/readiness endpoints
│   │   ├── voice.py                # Endpoints STT/TTS y consulta IA
│   │   ├── governance.py           # Endpoints de gobernanza
│   │   └── recommendations.py      # Endpoints de recomendaciones
│   └── services/
│       ├── gcp_service.py          # Integración GCP + Vertex AI
│       └── governance_service.py   # Reglas y análisis de compliance
├── tests/
│   ├── __init__.py
│   └── test_governance.py
├── scripts/
│   ├── run.sh                      # Arranque local del backend
│   ├── setup.sh                    # Setup GCP y entorno
│   ├── start_voice_client.sh       # Cliente de voz
│   ├── test_endpoints.sh           # Smoke test de endpoints
│   ├── deploy-gke.sh               # Deploy a GKE
│   └── show-structure.py
├── docs/                           # Documentación extendida
├── examples/
│   └── api_examples.py
├── deployment/
│   └── k8s/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── requirements-dev.txt
└── voice_client.py
```

## 🔧 Desarrollo

### Instalar Dependencias de Desarrollo

```bash
pip install -r requirements-dev.txt
```

### Ejecutar Tests

```bash
pytest tests/ -v --cov=src
```

### Linting y Formateo

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## 🤖 Funcionalidades del Asistente

### 1. Análisis de Gobernanza
- Verificación de cumplimiento de políticas
- Auditoría de accesos IAM
- Análisis de permisos excesivos
- Recomendaciones de seguridad

### 2. Buenas Prácticas DevOps
- Evaluación de configuración de CI/CD
- Análisis de infraestructura como código
- Recomendaciones de escalabilidad
- Optimización de costos en GCP

### 3. Procesamiento de Voz
- Reconocimiento de intenciones
- Generación de respuestas en texto
- Síntesis de voz natural

## 📚 Ejemplos de Uso

```bash
# Consultar sobre gobernanza de IAM
curl -X POST http://localhost:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{"resource_type": "iam", "resource_data": {"audit_logging_enabled": false}}'

# Obtener recomendaciones de buenas prácticas
curl -s http://localhost:8000/api/v1/recommendations/quick/security
```

## 🔐 Seguridad

- Autenticación con Google Cloud IAM
- Encriptación de datos sensibles
- Validación de inputs
- Rate limiting en endpoints
- Logging de todas las acciones

## 📊 Monitoreo

El proyecto incluye integración con:
- Cloud Logging (GCP)
- Cloud Monitoring (GCP)
- OpenTelemetry (opcional)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 📧 Soporte

Para preguntas o problemas, abre un issue en el repositorio.

---

**Última actualización**: 2026-01-22
