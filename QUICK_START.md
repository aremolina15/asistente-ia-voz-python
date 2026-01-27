# 🎯 Referencia Rápida - Asistente de Voz DevOps

## ⚡ Inicio Rápido

```bash
# Terminal 1: Servidor
cd $PROJECT_DIR  # Cambia a tu directorio del proyecto
source venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Cliente
cd $PROJECT_DIR  # Cambia a tu directorio del proyecto
python voice_client.py
```

## 🎤 Cómo Usar

1. **Sistema inicia:** Ver mensaje `🎤 Sistema listo. Habla ahora...`
2. **Hablar:** Di tu pregunta/comando
3. **Silencio:** Espera 2.5 segundos después de terminar
4. **Sistema procesa:** Verás `⏸️ Esperando respuesta de la IA...`
5. **Responde:** Se escucha audio con la respuesta
6. **Vuelve a escuchar:** Automáticamente disponible
7. **Repetir:** Habla nuevamente

## 📢 Ejemplos de Comandos

### Preguntas (Se agrega `?`)
```
"Qué es Terraform"           → "Qué es Terraform?"
"Cómo despliego en GCP"      → "Cómo despliego en GCP?"
"Dónde configuro un firewall" → "Dónde configuro un firewall?"
"Por qué falla mi deployment" → "Por qué falla mi deployment?"
```

### Comandos (Se agrega `.`)
```
"Instala Docker"             → "Instala Docker."
"Crea un cluster en Kubernetes" → "Crea un cluster en Kubernetes."
"Ejecuta el pipeline"        → "Ejecuta el pipeline."
```

## 📊 Línea de Tiempo

```
T=0s:    🎤 Grabando... habla ahora
T=1s:    [Usuario habla]
T=5s:    ✋ Fin de solicitud detectado (silencio detectado)
T=5.5s:  ⏳ Enviando a procesar...
T=5.5s:  ⏸️ Esperando respuesta de la IA...
T=6s:    📝 Transcribiendo...
T=7s:    👤 Tú: [pregunta limpia]
T=7.5s:  🤖 Procesando...
T=9s:    🗣️ Asistente: [respuesta]
T=9.5s:  🔊 Reproduciendo audio...
T=15s:   ✅ Respuesta completada
T=15s:   🎤 Sistema listo. Habla ahora...
```

## 🔧 Parámetros Ajustables

### En `voice_client.py` línea 20

```python
# Actual (normal):
record_audio_continuous(silence_threshold=0.012, silence_duration=2.5)

# Silencioso:
record_audio_continuous(silence_threshold=0.010, silence_duration=2.0)

# Ruidoso:
record_audio_continuous(silence_threshold=0.015, silence_duration=3.0)
```

### Variables de entorno

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/al/archivo.json"
export GOOGLE_CLOUD_PROJECT="tu-proyecto-gcp"
export VERTEX_AI_MODEL="gemini-2.0-flash"  # o gemini-2.5-flash
```

## ✅ Verificaciones

### ¿El servidor está corriendo?
```bash
curl http://localhost:8000/health
# Debe responder: {"status":"healthy",...}
```

### ¿Los endpoints funcionan?
```bash
./test_endpoints.sh
# Prueba /synthesize y /query
```

### ¿Las credenciales están OK?
```bash
ls -la "$GOOGLE_APPLICATION_CREDENTIALS"
# Debe existir el archivo
```

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| **Servidor no inicia** | `lsof -ti:8000 \| xargs -r kill -9` |
| **No se escucha audio** | Subir volumen con `alsamixer` |
| **IA no responde** | Verificar credenciales GCP |
| **Silencio no detecta** | Aumentar `silence_threshold` a 0.015 |
| **Interrupciones** | Aumentar `silence_duration` a 3.0 |

## 📁 Archivos Principales

| Archivo | Propósito |
|---------|-----------|
| `voice_client.py` | Cliente con escucha continua |
| `src/main.py` | Servidor FastAPI |
| `src/config.py` | Configuración GCP |
| `src/services/gcp_service.py` | Integración VertexAI/STT/TTS |
| `src/routers/voice.py` | Endpoints de voz |

## 🔄 Flujo de Datos

```
Micrófono
   ↓
record_audio_continuous()    ← Captura con silencio
   ↓
/api/v1/voice/transcribe     ← Speech-to-Text (GCP)
   ↓
clean_transcription()        ← Normaliza texto
   ↓
/api/v1/voice/query          ← VertexAI Gemini (procesa)
   ↓
Text-to-Speech (GCP)         ← Síntesis de voz
   ↓
ffplay response.mp3          ← Reproducción
   ↓
Altavoces
```

## 💡 Tips

1. **Habla claramente** - Mejor transcripción
2. **Frases cortas** - Más rápido procesamiento
3. **Temas DevOps** - IA enfocada en eso
4. **Espera silencio** - No interrumpas procesamiento
5. **Ctrl+C limpio** - Cierra correctamente

## 📈 Características

✅ Escucha continua
✅ Detección inteligente de silencio (2.5s)
✅ Comprensión de lenguaje natural
✅ Preguntas y comandos
✅ Respuesta automática en voz
✅ Sincronización sin interrupciones
✅ Soporte para español
✅ Integración VertexAI Gemini

## 🎓 Stack Tecnológico

- **Backend:** FastAPI + Python 3.12
- **Audio:** sounddevice, soundfile, ffmpeg
- **GCP:** Speech-to-Text, Text-to-Speech, VertexAI
- **Modelo:** Gemini 2.0 Flash
- **Concurrencia:** Threading (queue, event)

---

**Versión:** 2.1
**Estado:** ✅ Producción
**Último update:** 22 enero 2026
