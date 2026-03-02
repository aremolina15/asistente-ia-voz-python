# Cómo Cambiar la Voz del Asistente

## Ubicación del Código

El código de síntesis de voz está en:
```
src/services/gcp_service.py
Método: synthesize_speech() - líneas 110-145
```

## Voces Disponibles en Español (Google Cloud TTS)

### Neural2 (Más Naturales - Recomendadas)

| Código | Género | Descripción |
|--------|--------|-------------|
| `es-ES-Neural2-A` | Femenina | Natural, profesional |
| `es-ES-Neural2-B` | Masculina | Clara y profesional (actual) |
| `es-ES-Neural2-C` | Femenina | Más joven y energética |
| `es-ES-Neural2-D` | Femenina | Profesional formal |
| `es-ES-Neural2-E` | Femenina | Cálida y amigable |
| `es-ES-Neural2-F` | Masculina | Grave y autoritativa |

### Wavenet (Alta Calidad)

| Código | Género | Descripción |
|--------|--------|-------------|
| `es-ES-Wavenet-B` | Masculina | Alta calidad, natural |
| `es-ES-Wavenet-C` | Femenina | Alta calidad, natural |
| `es-ES-Wavenet-D` | Femenina | Alta calidad, profesional |

### Standard (Básicas)

| Código | Género | Descripción |
|--------|--------|-------------|
| `es-ES-Standard-A` | Femenina | Básica |
| `es-ES-Standard-B` | Masculina | Básica |

## Cómo Cambiar la Voz

### Paso 1: Abrir el archivo

```bash
nano src/services/gcp_service.py
# O con tu editor favorito
```

### Paso 2: Buscar la sección de voz (línea ~124)

```python
voice = texttospeech_v1.VoiceSelectionParams(
    language_code=language_code,
    name=f"{language_code}-Neural2-B",  # <--- CAMBIA AQUÍ
)
```

### Paso 3: Cambiar el código de voz

Reemplaza `Neural2-B` con cualquier código de la tabla. Ejemplos:

**Voz masculina grave:**
```python
name=f"{language_code}-Neural2-F",
```

**Voz femenina profesional:**
```python
name=f"{language_code}-Neural2-A",
```

**Voz femenina cálida:**
```python
name=f"{language_code}-Neural2-E",
```

## Personalización Avanzada

### Ajustar el Tono (Pitch)

```python
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=-5.0,  # <--- AJUSTA AQUÍ
    speaking_rate=1.0,
)
```

**Valores de pitch:**
- `20.0` - Muy agudo (voz infantil)
- `10.0` - Agudo
- `0.0` - Normal (por defecto)
- `-5.0` - Ligeramente grave
- `-10.0` - Grave
- `-20.0` - Muy grave (voz profunda)

### Ajustar la Velocidad (Speaking Rate)

```python
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=0.0,
    speaking_rate=1.2,  # <--- AJUSTA AQUÍ
)
```

**Valores de speaking_rate:**
- `0.25` - Muy lento
- `0.5` - Lento
- `0.75` - Ligeramente lento
- `1.0` - Normal (por defecto)
- `1.2` - Ligeramente rápido
- `1.5` - Rápido
- `2.0` - Muy rápido
- `4.0` - Extremadamente rápido

## Configuraciones Recomendadas

### Asistente Profesional Masculino (Actual)
```python
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="es-ES",
    name="es-ES-Neural2-B",
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=0.0,
    speaking_rate=1.0,
)
```

### Asistente Autoritativo (Voz Grave)
```python
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="es-ES",
    name="es-ES-Neural2-F",
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=-8.0,  # Más grave
    speaking_rate=0.95,  # Ligeramente más lento
)
```

### Asistente Amigable (Femenina)
```python
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="es-ES",
    name="es-ES-Neural2-E",
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=2.0,  # Ligeramente más agudo
    speaking_rate=1.1,  # Un poco más rápido
)
```

### Asistente Rápido y Eficiente
```python
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="es-ES",
    name="es-ES-Neural2-B",
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    pitch=0.0,
    speaking_rate=1.3,  # 30% más rápido
)
```

## Paso Final: Aplicar Cambios

Después de editar el archivo, reinicia el servidor:

```bash
# Detén el servidor (CTRL+C en la terminal donde corre)

# Reinicia:
cd "/home/aremol1/Documents/LABs Personal/ASSISTENT-DEVOPS-VOICE/asistente-ia-voz-python"
source .venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Probar Diferentes Voces

Puedes probar directamente con curl:

```bash
curl -X POST http://localhost:8000/api/v1/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola, soy tu asistente DevOps. ¿En qué puedo ayudarte?"}' \
  --output test_voice.mp3

# Reproducir
ffplay test_voice.mp3
```

## Soporte para Otros Idiomas

Si quieres usar otros idiomas, cambia el `language_code`:

```python
# Inglés estadounidense
language_code="en-US"
name="en-US-Neural2-J"  # Masculino

# Inglés británico
language_code="en-GB"
name="en-GB-Neural2-D"  # Masculino

# Francés
language_code="fr-FR"
name="fr-FR-Neural2-B"  # Masculino

# Portugués Brasil
language_code="pt-BR"
name="pt-BR-Neural2-B"  # Masculino
```

## Troubleshooting

### Error: "Voice not found"
- Verifica que el código de voz sea exacto (sensible a mayúsculas)
- Asegúrate de usar el formato: `{language_code}-Neural2-X`

### La voz suena robótica
- Usa voces `Neural2` en lugar de `Standard`
- Ajusta el `pitch` y `speaking_rate` para sonar más natural

### La voz es muy lenta/rápida
- Ajusta `speaking_rate` entre 0.9 y 1.2
- Valores extremos (< 0.5 o > 2.0) pueden sonar artificiales

## Referencias

- [Google Cloud TTS Voces](https://cloud.google.com/text-to-speech/docs/voices)
- [Audio Profiles](https://cloud.google.com/text-to-speech/docs/audio-profiles)
- [SSML Tags](https://cloud.google.com/text-to-speech/docs/ssml)

---

**Nota:** Este documento ha sido revisado y actualizado para asegurar la precisión de la información sobre las voces disponibles y los pasos de configuración.

**Última actualización:** 27 de enero de 2026

