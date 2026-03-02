# Asistente IA con Voz para DevOps

Asistente conversacional para equipos DevOps que combina voz, IA generativa y RAG para responder con contexto técnico real, recomendaciones prácticas y trazabilidad de fuentes.

## 🎯 Objetivo del Proyecto

Centralizar el conocimiento DevOps (estándares, Terraform, CI/CD, seguridad, service accounts, arquitectura) en un asistente de voz que responda en segundos con acciones ejecutables y contexto confiable.

## ✅ Beneficios

- **Menor tiempo de búsqueda**: respuestas inmediatas sobre prácticas y estándares internos.
- **Mejor consistencia técnica**: recomendaciones alineadas con gobernanza y buenas prácticas.
- **Menos riesgo operativo**: enfoque en mínimo privilegio, validaciones y rollback.
- **Experiencia natural**: interacción por voz y salida en español natural (configurada para `es-CO`).
- **Trazabilidad**: respuestas RAG con `sources` para auditoría del conocimiento utilizado.

## 🚀 Capacidades Actuales

- Consultas de voz end-to-end (STT → LLM/RAG → TTS).
- Motor RAG híbrido (vectorial + léxico) con modo estricto.
- Recomendaciones DevOps por contexto e infraestructura.
- Análisis de gobernanza (IAM, Storage, GKE) y compliance score.
- Persistencia de audios en Cloud Storage.
- Frontend web con micrófono en `/app` para demo y uso rápido.
- Respuesta natural en español (`es-CO` por defecto), con soporte configurable de voz.

## 🏗️ Arquitectura General

### Vista rápida

```
┌───────────────────┐      ┌──────────────────────────────┐      ┌────────────────────────────┐
│ Cliente de Voz    │ ---> │ API FastAPI                  │ ---> │ Servicios GCP + Vertex AI  │
│ voice_client.py   │      │ src/main.py + routers        │      │ STT, TTS, Gemini, Storage  │
└───────────────────┘      └──────────────┬───────────────┘      └──────────────┬─────────────┘
                                          │                                     │
                                          v                                     v
                                   ┌───────────────┐                    ┌──────────────────────┐
                                   │ RAG Pipeline  │ <----------------- │ Base de conocimiento │
                                   │ Chroma+Embeds │                    │          knowledge   │
                                   └───────────────┘                    └──────────────────────┘
```

### Capas del sistema

- **Interfaz**: `voice_client.py` (captura/procesa audio y consume API).
- **API**: `src/main.py` y routers en `src/routers/*`.
- **Servicios**: `src/services/gcp_service.py` y `src/services/governance_service.py`.
- **RAG**: `src/rag/ingest.py` y `src/rag/pipeline.py`.
- **Prompts**: `src/prompts/*` versionados por dominio.

### Flujo end-to-end

1. Usuario habla o envía texto.
2. `POST /api/v1/voice/transcribe` transcribe audio (Speech-to-Text).
3. `POST /api/v1/voice/query` resuelve con RAG (si está activo) o fallback LLM.
4. Se sintetiza respuesta con `POST /api/v1/voice/synthesize` (Text-to-Speech).
5. Se devuelve JSON + `audio_base64` + `sources` (si aplica RAG).

## 🧩 Componentes Principales

- **Orquestación API**: `src/main.py`
- **Router de voz**: `src/routers/voice.py`
- **Router de gobernanza**: `src/routers/governance.py`
- **Router de recomendaciones**: `src/routers/recommendations.py`
- **Health/Ready**: `src/routers/health.py` (`/health`, `/ready`)
- **Integración GCP + IA**: `src/services/gcp_service.py`
- **Reglas de gobernanza**: `src/services/governance_service.py`
- **RAG ingest**: `src/rag/ingest.py`
- **RAG retrieval/generación**: `src/rag/pipeline.py`

## 📋 Requisitos

- Python 3.10+
- Proyecto GCP con APIs habilitadas
- Credenciales válidas (`GOOGLE_APPLICATION_CREDENTIALS`)
- (Opcional) Docker / Kubernetes para despliegue

## ⚙️ Configuración de Entorno

### 1) Preparar entorno local

```bash
git clone https://github.com/aremolina15/asistente-ia-voz-python.git
cd asistente-ia-voz-python

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Variables de entorno

```bash
cp .env.example .env
```

Variables clave:

- `GOOGLE_CLOUD_PROJECT`
- `GCP_REGION`
- `GOOGLE_APPLICATION_CREDENTIALS`
- `RAG_ENABLED=true` (si quieres respuestas con contexto documental)
- `VOICE_DEFAULT_LANGUAGE_CODE=es-CO`

### 3) APIs GCP recomendadas

```bash
gcloud config set project TU_PROJECT_ID
gcloud services enable aiplatform.googleapis.com speech.googleapis.com texttospeech.googleapis.com storage.googleapis.com
```

## ▶️ Ejecución Correcta

### Backend

```bash
source .venv/bin/activate
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### Validación rápida

```bash
curl http://127.0.0.1:8000/health
```

> Si ves `curl: (7) Failed to connect`, el backend no está corriendo o está en otro puerto.

### Documentación interactiva

- `http://127.0.0.1:8000/docs`

### Frontend web con micrófono

- `http://127.0.0.1:8000/app`
- Permite grabar voz desde el navegador, transcribir, consultar IA/RAG y reproducir la respuesta en audio.

### Cliente de voz (opcional)

En otra terminal:

```bash
source .venv/bin/activate
python voice_client.py
```

### Script de arranque del cliente (opcional)

```bash
./scripts/start_voice_client.sh
```

## 🧠 Modo RAG

### Ingestar conocimiento

```bash
source .venv/bin/activate
python -m src.rag.ingest
```

### Qué hace el RAG actual

- Chunking estructurado para Markdown/YAML/Terraform/PDF.
- Embeddings con Vertex (`text-embedding-005`).
- Almacenamiento vectorial local con Chroma.
- Ranking híbrido por similitud + coincidencia de términos.
- Modo estricto configurable (`RAG_STRICT_MODE`, `RAG_MIN_LEXICAL_OVERLAP`).

## 📁 Estructura del Proyecto

```
asistente-ia-voz-python/
├── frontend/
│   └── index.html
├── src/
│   ├── main.py
│   ├── config.py
│   ├── prompts/
│   ├── rag/
│   │   ├── ingest.py
│   │   └── pipeline.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── voice.py
│   │   ├── governance.py
│   │   └── recommendations.py
│   └── services/
│       ├── gcp_service.py
│       └── governance_service.py
├── data/
│   ├── knowledge/
│   └── chroma/
├── scripts/
├── docs/
├── examples/
├── deployment/k8s/
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── voice_client.py
```

## 🧪 Endpoints Útiles

```bash
# Health
curl -s http://127.0.0.1:8000/health

# Consulta con voz/IA (texto)
curl -X POST http://127.0.0.1:8000/api/v1/voice/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Dame una recomendación de seguridad para Terraform","language_code":"es-CO"}'

# Gobernanza IAM
curl -X POST http://127.0.0.1:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{"resource_type":"iam","resource_data":{"audit_logging_enabled":false}}'
```

## 🔐 Seguridad (sin exponer secretos)

- Usa credenciales por variables de entorno y **no** hardcodees claves o tokens.
- No subas `.env`, llaves JSON, tokens de acceso ni credenciales temporales al repositorio.
- Configura `SECRET_KEY` y `ALLOWED_ORIGINS` para ambientes reales.
- Aplica mínimo privilegio para cuentas de servicio y revisa permisos periódicamente.
- Mantén trazabilidad en logs, evitando registrar datos sensibles en texto plano.

## ⚙️ Operación y despliegue

- Despliegue local: `uvicorn`, `docker-compose`, frontend en `/app`.
- Despliegue productivo: manifiestos en `deployment/k8s`.
- Documentación adicional de seguridad y revisión: `SECURITY.md` y `CODE_REVIEW_FINDINGS.md`.

## 🤝 Contribución

1. Crea rama de trabajo.
2. Implementa cambios con pruebas.
3. Abre Pull Request con resumen técnico.

---

**Última actualización**: 2026-03-02
