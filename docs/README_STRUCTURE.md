# 📁 Estructura del Proyecto - Asistente de Voz DevOps

```
asistente-ia-voz-python/
│
├── 📄 Archivos de Configuración
│   ├── .env                         # Variables de entorno (GCP credenciales)
│   ├── requirements.txt             # Dependencias Python
│   └── README.md                    # Documentación general
│
├── 🐍 Cliente Principal
│   └── voice_client.py              # Cliente CLI con escucha continua
│       ├── record_audio_continuous()        (línea 20)  - Grabación con silencio
│       ├── transcribe()                     (línea 75)  - STT
│       ├── clean_transcription()            (línea 88)  - Limpieza NLP
│       ├── query_ai()                       (línea 138) - Procesamiento IA
│       ├── process_audio_thread()           (línea 165) - Hilo de procesamiento
│       └── main()                           (línea 191) - Loop principal
│
├── 🔧 Servidor FastAPI
│   └── src/
│       ├── main.py                  # Servidor (host:8000)
│       │   ├── lifespan events
│       │   ├── /health endpoint
│       │   ├── /api/v1/voice router
│       │   ├── Governance & Recommendations endpoints
│       │   └── CORS middleware
│       │
│       ├── config.py                # Pydantic Settings
│       │   └── Configuración GCP (pydantic v2 compatible)
│       │
│       ├── routers/
│       │   └── voice.py             # Endpoints de voz
│       │       ├── POST /transcribe  - Speech-to-Text
│       │       ├── POST /synthesize  - Text-to-Speech
│       │       └── POST /query       - Procesamiento completo
│       │
│       └── services/
│           └── gcp_service.py       # Integraciones GCP
│               ├── TranscriberService      (Speech-to-Text)
│               ├── SynthesisService       (Text-to-Speech)
│               ├── GenerativeModel        (VertexAI Gemini)
│               └── System Instruction     (DevOps context)
│
├── 📚 Documentación
│   ├── QUICK_START.md               # Inicio rápido (5 min)
│   ├── README_MEJORAS.md            # Guía detallada v2.0
│   ├── UPGRADE_v2.1.md              # Detalles técnicos v2.1
│   ├── RESUMEN_FINAL.md             # Visión general del proyecto
│   ├── MEJORAS_v2.md                # Especificación v2.0
│   ├── CHANGELOG.md                 # Historial de versiones
│   └── README_STRUCTURE.md          # Este archivo
│
├── 🔨 Scripts de Utilidad
│   ├── start_voice_client.sh        # Inicio automático del cliente
│   ├── test_endpoints.sh            # Prueba de endpoints (sin micrófono)
│   ├── start.sh                     # Inicio del servidor
│   ├── run.sh                       # Wrapper de ejecución
│   ├── setup.sh                     # Setup inicial
│   └── deploy-gke.sh                # Despliegue en Kubernetes
│
└── 📦 Directorio de Entorno Virtual
    └── venv/                        # Python 3.12 virtualenv
        ├── bin/activate
        ├── lib/python3.12/site-packages/
        └── [dependencias instaladas]
```

## 📊 Dependencias Principales

### Backend (FastAPI)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### GCP & IA
```
google-cloud-speech==2.21.0
google-cloud-texttospeech==2.14.1
google-cloud-aiplatform==1.40.0
vertexai==0.28.0
```

### Audio
```
sounddevice==0.4.6
soundfile==0.12.1
numpy==1.24.0
```

### Utilidades
```
python-dotenv==1.0.0
requests==2.31.0
```

## 🔄 Flujo de Datos

```
Cliente (voice_client.py)              Servidor (src/main.py)
═════════════════════════════════════════════════════════════

record_audio_continuous()              
    ↓ (WAV binary)                     
    └─────────────────→ POST /transcribe
                            ↓
                       gcp_service.py
                       Speech-to-Text (GCP)
                            ↓ (transcript string)
                       ← Respuesta JSON
    ↓ (Transcripción)
    
clean_transcription()
    ↓ (Texto limpio)
    
query_ai()
    ├─ clean_transcription() + IA
    ├─ POST /query (Gemini)
    │    ↓
    │   gcp_service.py
    │   ├─ Gemini 2.0 Flash
    │   ├─ Text-to-Speech (GCP)
    │   └─ base64 MP3 encoding
    │    ↓
    │   ← JSON response
    │       ├─ "response": string
    │       └─ "audio_base64": string
    ↓
    
Decode base64 → response.mp3
    ↓
ffplay response.mp3 (foreground)
    ↓
Loop vuelve a escuchar
```

## 🎯 Puntos de Sincronización

### v2.1 - Threading Model

```
MAIN THREAD (Thread Principal)
├─ record_audio_continuous()         [BLOQUEANTE]
│   └─ Espera 2.5s de silencio
├─ processing_done.clear()           [RESET]
├─ response_queue.put(wav)           [ENVÍA]
├─ processing_done.wait()            [BLOQUEANTE] ← NUEVO EN v2.1
└─ Vuelve a grabar

PROCESS THREAD (Hilo de Procesamiento)
├─ response_queue.get()              [ESPERA AUDIO]
├─ transcribe()
├─ query_ai()
│   ├─ Gemini
│   └─ Text-to-Speech
├─ ffplay (foreground)               [ESPERA AUDIO]
└─ processing_done.set()             [SEÑAL] ← DESBLOQUEA wait()
```

## 🔐 Configuración GCP

### Variables de Entorno (.env)
```
GOOGLE_CLOUD_PROJECT=tu-proyecto-gcp
GCP_REGION=us-central1
VERTEX_AI_MODEL=gemini-2.0-flash
GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/credentials.json
SPEECH_TO_TEXT_ENABLED=true
TEXT_TO_SPEECH_ENABLED=true
```

### APIs Requeridas
- ✅ Cloud Speech-to-Text API
- ✅ Cloud Text-to-Speech API
- ✅ Vertex AI API
- ✅ Cloud Logging API

## 📈 Métricas de Complejidad

| Componente | LOC | Complejidad | Versión |
|-----------|-----|-------------|---------|
| voice_client.py | 220 | Media | v2.1 |
| src/main.py | ~150 | Baja | v1.0 |
| src/config.py | ~30 | Baja | v1.0 |
| src/services/gcp_service.py | ~200 | Alta | v2.0 |
| src/routers/voice.py | ~100 | Media | v2.0 |
| **Total** | **~700** | **Media** | v2.1 |

## 🧪 Puntos de Prueba

### Test Manual
```bash
# Terminal 1: Servidor
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Cliente
python voice_client.py
```

### Test Automatizado
```bash
# Sin micrófono
./test_endpoints.sh
```

### Verificaciones
```bash
# Salud del servidor
curl http://localhost:8000/health

# Verificar compilación
python -m py_compile voice_client.py
python -m py_compile src/*.py src/*/*.py
```

## 🚀 Despliegue

### Local
```bash
./start_voice_client.sh
```

### Producción (Kubernetes)
```bash
./deploy-gke.sh
```

## 📝 Notas

1. **Sincronización**: El cambio principal en v2.1 es `threading.Event()` para esperar respuesta
2. **Audio**: Cambiar de background (`&`) a foreground es crítico para UX
3. **Seguridad**: Las credenciales GCP deben estar en `.env` (no en código)
4. **Rendimiento**: Gemini 2.0 Flash es rápido y económico
5. **Idioma**: Sistema completamente en español

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| Puerto ocupado | `lsof -ti:8000 \| xargs -r kill -9` |
| Sin audio | Revisar volumen del sistema |
| Credenciales | Verificar `GOOGLE_APPLICATION_CREDENTIALS` |
| Lentitud | Aumentar verbosidad en logs |

---

**Última actualización:** 22 de Enero, 2026
**Versión del Documento:** 2.1
**Mantenedor:** Equipo DevOps
