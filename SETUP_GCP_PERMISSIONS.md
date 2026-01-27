# Configuración de Permisos GCP para VertexAI

## Problema
Error 403 al intentar usar VertexAI Gemini:
```
Permission 'aiplatform.endpoints.predict' denied on resource
```

## Solución

### Paso 1: Exportar la clave de la cuenta de servicio

**Desde la consola GCP:**
1. Ve a **IAM & Admin** → **Service Accounts**
2. Busca y haz clic en: `heroic-dolphin-455016-q8@appspot.gserviceaccount.com`
3. Ve a la pestaña **Keys**
4. Haz clic en **Create new key** → **JSON**
5. Se descargará `service-account-key.json`

**O desde terminal:**
```bash
gcloud iam service-accounts keys create appengine-sa-key.json \
  --iam-account=heroic-dolphin-455016-q8@appspot.gserviceaccount.com
```

### Paso 2: Agregar la ruta en `.env`

Asegúrate que tu `.env` tenga:
```env
GOOGLE_APPLICATION_CREDENTIALS=./appengine-sa-key.json
GOOGLE_CLOUD_PROJECT=heroic-dolphin-455016-q8
GCP_REGION=us-central1
```

### Paso 3: Asignar el rol `aiplatform.user`

Ejecuta este comando en terminal:
```bash
gcloud projects add-iam-policy-binding heroic-dolphin-455016-q8 \
  --member=serviceAccount:heroic-dolphin-455016-q8@appspot.gserviceaccount.com \
  --role=roles/aiplatform.user
```

### Paso 4: Verificar que se asignó

```bash
gcloud projects get-iam-policy heroic-dolphin-455016-q8 \
  --flatten="bindings[].members" \
  --filter="bindings.role:aiplatform.user"
```

Deberías ver:
```
- serviceAccount:heroic-dolphin-455016-q8@appspot.gserviceaccount.com
```

### Paso 5: Esperar y reiniciar el servidor

Los permisos pueden tardar **1-2 minutos** en propagarse. Luego:

```bash
# Detén el servidor actual (CTRL+C)

# Reinicia:
cd "/home/aremol1/Documents/LABs Personal/ASSISTENT-DEVOPS-VOICE/asistente-ia-voz-python"
source .venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 6: Probar

```bash
# En otra terminal:
curl -X POST http://localhost:8000/health
```

Deberías obtener una respuesta sin errores 403.

## Troubleshooting

### Error: "Invalid service account key"
- Verifica que `appengine-sa-key.json` esté en el directorio raíz del proyecto
- Verifica que `GOOGLE_APPLICATION_CREDENTIALS` apunte correctamente en `.env`

### Error: "Permission denied" persiste
- Espera 2-3 minutos más (propagación de IAM)
- Limpia cache: `rm -rf ~/.cache/gcloud`
- Reautentica: `gcloud auth application-default login`

### Error: "Resource not found"
- Verifica que el modelo `gemini-2.0-flash` esté disponible en tu región (`us-central1`)
- Intenta con `gemini-pro` como alternativa en `.env`:
  ```env
  VERTEX_AI_MODEL=gemini-pro
  ```

## Roles disponibles

| Rol | Descripción |
|-----|-------------|
| `roles/aiplatform.user` | Acceso básico a VertexAI (recomendado) |
| `roles/aiplatform.admin` | Control total (no recomendado) |
| `roles/ml.developer` | Para ML/IA en general |
| `roles/editor` | Acceso completo (muy permisivo) |

## Archivos involucrados

```
asistente-ia-voz-python/
├── .env                        # Variables de entorno
├── appengine-sa-key.json       # Credenciales GCP (NO SUBIR A GIT)
├── src/
│   ├── config.py               # Lee GOOGLE_APPLICATION_CREDENTIALS
│   └── services/
│       └── gcp_service.py      # Usa VertexAI
└── .gitignore                  # Debe incluir: appengine-sa-key.json
```

## Seguridad

⚠️ **IMPORTANTE:**
- **Nunca** subas `appengine-sa-key.json` a Git
- Verifica que esté en `.gitignore`:
  ```
  appengine-sa-key.json
  *.json
  ```
- La clave tiene acceso a tu proyecto GCP

---

**Última actualización:** 27 enero 2026


Servicios que tu asistente consume activamente:
Servicio	Uso	Cuándo se usa
Speech-to-Text	Transcripción de audio	Cada vez que hablas
Text-to-Speech	Síntesis de voz	Cada respuesta del asistente
Vertex AI (Gemini)	Generación de respuestas	Procesamiento de consultas
Cloud Logging	Registro de eventos	Siempre (background)
Cloud Storage	(Opcional) Almacenamiento	Si guardas audios
