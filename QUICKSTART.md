# Guía de Inicio Rápido

## 🚀 Instalación en 5 Minutos

### 1. Requisitos Previos
```bash
# Verificar Python 3.10+
python --version

# Verificar gcloud CLI
gcloud --version
```

### 2. Configuración de GCP
```bash
# Autorizar gcloud
gcloud auth login

# Crear un proyecto (opcional)
gcloud projects create devops-voice-assistant
gcloud config set project devops-voice-assistant

# Habilitar APIs
gcloud services enable \
    speech.googleapis.com \
    texttospeech.googleapis.com \
    aiplatform.googleapis.com
```

### 3. Setup del Proyecto
```bash
# Clonar repositorio
git clone https://github.com/aremolina15/asistente-ia-voz-python.git
cd asistente-ia-voz-python

# Ejecutar setup script
chmod +x setup.sh
./setup.sh YOUR-PROJECT-ID

# Activar entorno virtual
source venv/bin/activate
```

### 4. Ejecutar la Aplicación
```bash
# Modo desarrollo
python -m uvicorn src.main:app --reload

# La API estará en: http://localhost:8000
# Documentación: http://localhost:8000/docs
```

## 📋 Primeros Pasos

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Análisis de Gobernanza
```bash
curl -X POST http://localhost:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "iam",
    "resource_data": {
      "service_accounts": [1, 2, 3],
      "bindings": {"user@example.com": ["Editor", "Viewer"]},
      "uses_custom_roles": false,
      "audit_logging_enabled": true
    }
  }'
```

### Test 3: Recomendaciones Rápidas
```bash
curl http://localhost:8000/api/v1/recommendations/quick/security
```

### Test 4: Consulta de Voz (Ejemplo)
```bash
curl -X POST http://localhost:8000/api/v1/voice/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Cuáles son las mejores prácticas para IAM en GCP?",
    "language_code": "es-ES"
  }'
```

## 🐳 Con Docker

```bash
# Construir imagen
docker build -t devops-voice:latest .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  devops-voice:latest

# O con docker-compose
docker-compose up
```

## ☸️ En Kubernetes (GKE)

```bash
# Desplegar
./deploy-gke.sh your-project-id cluster-name us-central1

# Verificar despliegue
kubectl get pods -n devops
kubectl logs -f deployment/devops-voice-assistant -n devops

# Acceder a la API
kubectl port-forward svc/devops-voice-assistant 8000:8000 -n devops
```

## 📚 Ejemplos Prácticos

### Analizar Configuración de Storage
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/governance/analyze",
    json={
        "resource_type": "storage",
        "resource_data": {
            "encryption_enabled": True,
            "versioning_enabled": False,  # Problema
            "lifecycle_policy": None,      # Problema
            "is_public": False,
            "audit_logging_enabled": True
        },
        "include_recommendations": True
    }
)

print(response.json())
```

### Obtener Assessment de Infraestructura
```python
import requests

infra_config = {
    "clusters": 2,
    "nodes": 10,
    "services": 50,
    "databases": 3,
    "storage_buckets": 15
}

response = requests.post(
    "http://localhost:8000/api/v1/recommendations/infrastructure-assessment",
    json=infra_config
)

print(response.json())
```

## 🔧 Configuración

### Variables de Entorno Importantes
```bash
# .env
GOOGLE_CLOUD_PROJECT=your-project-id
GCP_REGION=us-central1
VERTEX_AI_MODEL=gemini-1.5-pro
STORAGE_BUCKET=your-bucket-name
LOG_LEVEL=INFO
DEBUG=False
```

## 🐛 Troubleshooting

### Error: "No credentials found"
```bash
# Solución
gcloud auth application-default login
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Error: "API not enabled"
```bash
# Solución: Habilitar la API en GCP
gcloud services enable speech.googleapis.com
```

### Error de conexión a GCP
```bash
# Verificar credenciales
gcloud auth list

# Reautenticar
gcloud auth login
```

## 📖 Documentación

- [Arquitectura](ARCHITECTURE.md)
- [API Documentation](http://localhost:8000/docs) (después de ejecutar)
- [Google Cloud Documentation](https://cloud.google.com/docs)

## 🆘 Necesitas Ayuda?

1. Revisa los logs: `tail -f logs/*.log`
2. Documentación: Consulta `ARCHITECTURE.md`
3. Crea un issue en GitHub
4. Contacta al equipo de soporte

## ✅ Checklist de Validación

- [ ] Python 3.10+ instalado
- [ ] gcloud CLI configurado
- [ ] Proyecto GCP creado
- [ ] APIs habilitadas en GCP
- [ ] Variables de entorno en .env
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Health check pasando (`curl http://localhost:8000/health`)
- [ ] Documentación accesible (`http://localhost:8000/docs`)

¡Listo! Ya tienes el asistente IA con voz para DevOps ejecutándose. 🎉
