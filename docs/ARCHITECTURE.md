# Arquitectura del Asistente IA con Voz para DevOps

## 🏗️ Componentes Principales

### 1. **API REST (FastAPI)**
- Framework moderno con validación automática
- Documentación Swagger interactiva (`/docs`)
- CORS configurado para desarrollo
- Manejo de errores centralizado

### 2. **Servicios GCP**
- **Speech-to-Text**: Convierte audio a texto
- **Text-to-Speech**: Sintetiza voz natural
- **VertexAI Gemini**: Motor de IA para análisis
- **Cloud Storage**: Almacenamiento de archivos
- **Cloud Logging**: Auditoría de acciones

### 3. **Motores de Análisis**
- **Gobernanza**: Evalúa políticas y compliance
- **Buenas Prácticas**: Recomendaciones DevOps
- **Risk Assessment**: Evaluación de seguridad

## 🔄 Flujo de Procesamiento

```
1. Input de Voz
   ↓
2. Speech-to-Text (GCP)
   ↓
3. Procesamiento de Intent
   ↓
4. Selección de Motor (Gobernanza/Buenas Prácticas)
   ↓
5. Análisis con VertexAI
   ↓
6. Text-to-Speech (GCP)
   ↓
7. Output de Voz + Respuesta JSON
```

## 📊 Endpoints Principales

### Health
- `GET /health` - Health check
- `GET /ready` - Readiness check

### Voz
- `POST /api/v1/voice/transcribe` - Transcribir audio
- `POST /api/v1/voice/synthesize` - Sintetizar voz
- `POST /api/v1/voice/query` - Consulta completa de voz

### Gobernanza
- `POST /api/v1/governance/analyze` - Analizar gobernanza
- `GET /api/v1/governance/best-practices/{resource_type}` - Obtener prácticas
- `POST /api/v1/governance/compliance-report` - Reporte de compliance

### Recomendaciones
- `POST /api/v1/recommendations/devops` - Recomendaciones DevOps
- `GET /api/v1/recommendations/quick/{topic}` - Recomendaciones rápidas
- `POST /api/v1/recommendations/infrastructure-assessment` - Assessment

## 🔐 Seguridad

### Autenticación
- Google Cloud IAM para autorización
- Service Account para aplicación
- RBAC en Kubernetes

### Encriptación
- TLS en tránsito
- Encriptación de datos en GCP
- Variables sensibles en .env

### Auditoría
- Cloud Logging de todas las acciones
- Trazabilidad de análisis
- Logs estructurados

## 🚀 Deployment Options

### 1. Local (Desarrollo)
```bash
python -m uvicorn src.main:app --reload
```

### 2. Docker
```bash
docker-compose up
```

### 3. Kubernetes (GKE)
```bash
./deploy-gke.sh <project-id> <cluster> <region>
```

### 4. Cloud Run
```bash
gcloud run deploy devops-voice-assistant \
  --source . \
  --platform managed \
  --region us-central1
```

## 📈 Escalabilidad

### Horizontal
- Múltiples réplicas en Kubernetes
- Auto-scaling basado en CPU/memoria
- Load balancing

### Vertical
- Optimización de recursos
- Caché con Redis
- Indexación de búsquedas

## 🔍 Monitoreo

### Métricas
- Latencia de requests
- Tasa de error
- Uso de recursos
- Tokens consumidos (VertexAI)

### Logs
- Cloud Logging
- OpenTelemetry (opcional)
- Structured logging

### Alertas
- Cloud Monitoring
- Notificaciones por email/Slack
- SLO tracking

## 🧪 Testing

### Unitarios
```bash
pytest tests/test_governance.py
```

### Integración
```bash
pytest tests/ -v --cov=src
```

### E2E
```bash
# Requiere ambiente configurado
python scripts/e2e_tests.py
```

## 📦 Dependencias Principales

- **fastapi**: Framework web
- **google-cloud-***: SDK de GCP
- **vertexai**: IA Gemini
- **pydantic**: Validación
- **pytest**: Testing

## 🛠️ Desarrollo

### Setup
```bash
./setup.sh <project-id>
```

### Formato de código
```bash
black src/ tests/
isort src/ tests/
```

### Linting
```bash
flake8 src/ tests/
mypy src/
```

## 📝 Flujo de Trabajo Típico

1. **Usuario hace consulta de voz**: "¿Cómo mejorar la seguridad de mi IAM?"
2. **Sistema transcribe**: Speech-to-Text
3. **Análisis de intent**: Gobernanza + Seguridad
4. **Consulta VertexAI**: Genera recomendaciones específicas
5. **Síntesis de voz**: Respuesta audible
6. **Retorno**: JSON + Audio MP3

## 🤖 Capacidades de IA

### Análisis
- Evaluación de configuraciones
- Detección de vulnerabilidades
- Análisis de compliance

### Recomendaciones
- Paso a paso de implementación
- Priorización automática
- Contexto específico de GCP

### Aprendizaje
- Mejora contínua
- Feedback de usuarios
- Actualización de modelos

## 🔗 Integración con Sistemas

### Webhooks
- Notificaciones de eventos
- Alertas automáticas
- Actualizaciones en tiempo real

### APIs de Terceros
- Slack integration
- JIRA integration
- Cloud Monitoring

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google Cloud Speech](https://cloud.google.com/speech-to-text/docs)
- [VertexAI Gemini](https://cloud.google.com/vertex-ai/docs/generative-ai)
- [Kubernetes en GKE](https://cloud.google.com/kubernetes-engine/docs)
