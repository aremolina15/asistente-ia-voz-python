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

```
┌─────────────────────────────────────────────────────────────┐
│                    Cliente (Web/CLI)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            FastAPI Backend (Python)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Voice Input Processing                             │  │
│  │ • NLP & Intent Recognition                           │  │
│  │ • Governance Analysis Engine                         │  │
│  │ • Best Practices Engine                              │  │
│  │ • Response Generation                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐         ┌──────────────┐      ┌──────────────┐
   │   GCP   │         │   VertexAI   │      │  Cloud       │
   │ Storage │         │   / Gemini   │      │  Logging     │
   │  & IAM  │         │              │      │              │
   └─────────┘         └──────────────┘      └──────────────┘
```

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
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── config.py               # Configuración de la app
│   ├── models/
│   │   ├── __init__.py
│   │   ├── governance.py       # Modelos de gobernanza
│   │   ├── best_practices.py   # Modelos de buenas prácticas
│   │   └── devops_rules.py     # Reglas DevOps
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gcp_service.py      # Integración GCP
│   │   ├── voice_service.py    # Procesamiento de voz
│   │   ├── ai_service.py       # Motor de IA (VertexAI)
│   │   ├── governance_service.py
│   │   └── logger_service.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py           # Health checks
│   │   ├── voice.py            # Endpoints de voz
│   │   ├── governance.py       # Endpoints de gobernanza
│   │   └── recommendations.py  # Endpoints de recomendaciones
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py          # Esquemas de request
│   │   └── response.py         # Esquemas de response
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_voice.py
│   ├── test_governance.py
│   └── test_ai_service.py
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── k8s/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
├── .env.example
├── requirements.txt
├── requirements-dev.txt
└── setup.py
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
curl -X POST http://localhost:8000/api/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{"resource": "projects/my-project/roles/custom_role", "type": "iam"}'

# Obtener recomendaciones de buenas prácticas
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"infrastructure": "kubernetes", "area": "security"}'
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
