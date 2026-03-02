# 🚀 GUÍA DE EJECUCIÓN - DevOps Voice Assistant

## Estado Actual

✅ **Proyecto creado exitosamente**  
✅ **Servidor ejecutándose**  
✅ **Dependencias instalándose**  

El servidor se está **iniciando en background**. Espera a que complete la instalación de dependencias.

---

## 📋 Lo Que Está Pasando Ahora

```
1. ✅ Creando/activando entorno virtual Python
2. ⏳ Instalando dependencias (FastAPI, GCP, VertexAI, etc.)
3. 🚀 Iniciando servidor FastAPI en puerto 8000
```

---

## 🌐 Cómo Acceder a la API

Una vez que el servidor esté listo (en ~1-2 minutos):

### **Opción 1: Interfaz Web (Recomendado)**
```
🔗 http://localhost:8000/docs
```
Aquí puedes probar todos los endpoints directamente.

### **Opción 2: Red docs
```
🔗 http://localhost:8000/redoc
```
Documentación en formato alternativo.

### **Opción 3: Health Check**
```bash
curl http://localhost:8000/health
```

---

## 🧪 Primeros Tests

### **Test 1: Verificar Estado**
```bash
curl -s http://localhost:8000/ | python -m json.tool
```

### **Test 2: Análisis de Gobernanza IAM**
```bash
curl -X POST http://localhost:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "iam",
    "resource_data": {
      "service_accounts": [1, 2, 3],
      "bindings": {"user@example.com": ["Editor"]},
      "uses_custom_roles": false,
      "audit_logging_enabled": true
    }
  }'
```

### **Test 3: Recomendaciones Rápidas**
```bash
curl http://localhost:8000/api/v1/recommendations/quick/security
```

---

## 📚 Scripts Útiles

### **Ejecutar Ejemplos**
```bash
cd $PROJECT_DIR  # O la ruta de tu proyecto
source venv/bin/activate
python examples.py
```

### **Ver Estructura del Proyecto**
```bash
python show-structure.py
```

### **Ejecutar Tests**
```bash
pytest tests/ -v
```

### **Ver Ayuda de Makefile**
```bash
make help
```

---

## ⚙️ Configuración (Si Necesitas Cambiar)

El archivo `.env` debe estar configurado con:
- **Proyecto GCP**: Tu ID de proyecto GCP
- **Región**: `us-central1` (o tu región preferida)
- **Debug Mode**: Configurable según entorno
- **Log Level**: `INFO`

Si necesitas cambiar algo, edita el archivo `.env` en la raíz del proyecto.

---

## 🔐 Configuración de GCP (Importante)

Si usas las funciones de voz (Speech-to-Text, Text-to-Speech, VertexAI), necesitas:

```bash
# Autenticar con tu cuenta de GCP
gcloud auth application-default login

# O usar una service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/governance/best-practices/{type}` | Buenas prácticas |
| `POST` | `/api/v1/governance/analyze` | Analizar gobernanza |
| `POST` | `/api/v1/governance/compliance-report` | Reporte de compliance |
| `GET` | `/api/v1/recommendations/quick/{topic}` | Recomendaciones rápidas |
| `POST` | `/api/v1/recommendations/devops` | Recomendaciones avanzadas |
| `POST` | `/api/v1/recommendations/infrastructure-assessment` | Assessment de infraestructura |

---

## 🐛 Troubleshooting

### **Error: "Cannot connect to localhost:8000"**
→ El servidor aún está iniciando. Espera 2 minutos más.

### **Error: "No credentials found"**
→ Ejecuta: `gcloud auth application-default login`

### **Error: "API not enabled"**
→ Habilita en GCP:
```bash
gcloud services enable speech.googleapis.com texttospeech.googleapis.com aiplatform.googleapis.com
```

### **Error: Dependencias no instalan**
→ Revisa el archivo `.env` y asegúrate de que el proyecto GCP es correcto.

---

## 📁 Estructura Importante

```
asistente-ia-voz-python/
├── src/main.py          ← Punto de entrada
├── src/services/        ← Lógica de negocio
├── src/routers/         ← Endpoints API
├── .env                 ← Variables de entorno
├── requirements.txt     ← Dependencias
└── run.sh              ← Script de ejecución
```

---

## 🎯 Próximos Pasos

### **Ahora Mismo (Esperar)**
1. El servidor está instalando dependencias
2. Debería estar listo en ~1-2 minutos
3. Abre http://localhost:8000/docs

### **Después (Próximas Acciones)**
1. Prueba los endpoints en la UI interactiva
2. Ejecuta los ejemplos: `python examples.py`
3. Lee la documentación: [ARCHITECTURE.md](ARCHITECTURE.md)
4. Explora el código en `src/`

---

## 💡 Consejos Útiles

✅ La documentación interactiva está en `/docs`  
✅ Puedes probar endpoints directamente sin instalar herramientas  
✅ El servidor reinicia automáticamente al editar código  
✅ Los logs se muestran en la terminal  

---

## ❓ ¿Preguntas?

Revisa:
- [README.md](README.md) - Descripción general
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida
- [ARCHITECTURE.md](ARCHITECTURE.md) - Diseño técnico
- http://localhost:8000/docs - Documentación interactiva

---

**Fecha**: 2026-01-22  
**Estado**: ✅ Servidor iniciando...


cd "/home/aremol1/Documents/LABs Personal/ASSISTENT-DEVOPS-VOICE/asistente-ia-voz-python" && export GOOGLE_APPLICATION_CREDENTIALS="$PWD/appengine-sa-key.json" && export GOOGLE_CLOUD_PROJECT="heroic-dolphin-455016-q8" && "/home/aremol1/Documents/LABs Personal/ASSISTENT-DEVOPS-VOICE/asistente-ia-voz-python/.venv/bin/python" voice_client.py