# 🎉 ¡SERVIDOR EJECUTÁNDOSE! - GUÍA DE USO

## ✅ Estado Actual

```
✅ SERVIDOR ACTIVO EN: http://localhost:8000
✅ HEALTH CHECK: RESPONDIENDO CORRECTAMENTE
✅ API DOCUMENTACIÓN: http://localhost:8000/docs
```

---

## 🚀 ¿QUÉ NECESITAS HACER AHORA?

### 1. **Abre la Interfaz Web (Lo más fácil)**

```
🌐 Dirección: http://localhost:8000/docs
```

Desde ahí puedes:
- Ver toda la documentación
- Probar todos los endpoints
- Enviar requests sin usar comandos

---

## 🧪 Ejemplos de Uso (Por Comandos)

### **Ejemplo 1: Verificar Estado**
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-22T15:24:27.919454",
  "service": "DevOps Voice Assistant"
}
```

---

### **Ejemplo 2: Análisis de Gobernanza IAM**

```bash
curl -X POST http://localhost:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "iam",
    "resource_data": {
      "service_accounts": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      "bindings": {"user@example.com": ["Editor", "Admin"]},
      "uses_custom_roles": false,
      "audit_logging_enabled": false
    }
  }'
```

**Respuesta:**
```json
{
  "resource_type": "iam",
  "risk_level": "alto",
  "findings": [
    {
      "severity": "medium",
      "issue": "Demasiadas cuentas de servicio",
      "recommendation": "Reducir a máximo 10 cuentas"
    },
    {
      "severity": "high",
      "issue": "Audit Logging no habilitado",
      "recommendation": "Habilitar Cloud Audit Logs"
    }
  ],
  "compliance_score": 70,
  "recommendations": []
}
```

---

### **Ejemplo 3: Recomendaciones Rápidas de Seguridad**

```bash
curl http://localhost:8000/api/v1/recommendations/quick/security
```

**Respuesta:**
```json
{
  "topic": "security",
  "recommendations": [
    "Habilitar Cloud Audit Logs",
    "Usar Cloud KMS para gestión de claves",
    "Implementar VPC Service Controls",
    "Usar Private Google Access",
    "Habilitar Cloud Security Command Center"
  ],
  "count": 5
}
```

---

### **Ejemplo 4: Análisis de Storage**

```bash
curl -X POST http://localhost:8000/api/v1/governance/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "storage",
    "resource_data": {
      "encryption_enabled": true,
      "versioning_enabled": false,
      "is_public": false,
      "audit_logging_enabled": false
    }
  }'
```

---

### **Ejemplo 5: Buenas Prácticas para un Recurso**

```bash
curl http://localhost:8000/api/v1/governance/best-practices/gke
```

---

## 📊 Todos los Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Verificar estado |
| `GET` | `/api/v1/governance/best-practices/{type}` | Buenas prácticas (iam, storage, gke) |
| `POST` | `/api/v1/governance/analyze` | Analizar gobernanza |
| `GET` | `/api/v1/recommendations/quick/{topic}` | Recomendaciones rápidas (security, performance, cost, scalability, reliability) |
| `POST` | `/api/v1/recommendations/devops` | Recomendaciones personalizadas |

---

## 🎯 Tareas Próximas

### **Paso 1: Explorar la UI (RECOMENDADO)**
```
🌐 http://localhost:8000/docs
```
- Es la forma más fácil
- Interfaz interactiva
- Prueba todos los endpoints
- Ve ejemplos de requests/responses

### **Paso 2: Instalar Dependencias Completas (Opcional)**
Si quieres usar todas las funciones de voz:
```bash
cd $PROJECT_DIR  # Cambia a tu directorio del proyecto
source venv/bin/activate
pip install google-cloud-speech google-cloud-texttospeech google-cloud-aiplatform vertexai
```

### **Paso 3: Configurar GCP (Si Usas Voz)**
```bash
gcloud auth application-default login
```

### **Paso 4: Editar Código**
El servidor **recarga automáticamente** cuando cambias el código.

---

## 📁 Archivos Importantes

```
<directorio-del-proyecto>/

├── src/main.py          ← El servidor (endpoints aquí)
├── .env                 ← Variables de entorno
├── requirements.txt     ← Dependencias
├── server.log           ← Logs del servidor
├── README.md            ← Documentación general
├── ARCHITECTURE.md      ← Diseño técnico
└── RUNNING.md           ← Guía de ejecución
```

---

## 🛑 Para Detener el Servidor

```bash
pkill -f "uvicorn src.main:app"
```

O simplemente cierra la terminal donde está corriendo.

---

## 🔍 Ver los Logs

```bash
cd $PROJECT_DIR  # Cambia a tu directorio del proyecto
tail -f server.log
```

---

## 🐍 Scripts Python

### Ejecutar ejemplos:
```bash
cd $PROJECT_DIR  # Cambia a tu directorio del proyecto
source venv/bin/activate
python examples.py
```

### Ver estructura:
```bash
python show-structure.py
```

---

## 📚 Documentación Completa

- [README.md](../README.md) - Descripción general
- [QUICKSTART.md](../QUICKSTART.md) - Inicio rápido
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Diseño técnico
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Cómo contribuir

---

## 🎓 Próximos Pasos Recomendados

1. ✅ **Ahora**: Abre http://localhost:8000/docs
2. 📝 **Próximo**: Prueba los endpoints en la UI
3. 🔧 **Luego**: Instala dependencias de GCP si necesitas voz
4. 📖 **Después**: Lee la documentación
5. 💻 **Final**: Personaliza el código

---

## 💡 Tips

✅ La documentación interactiva es la mejor forma de aprender  
✅ Todos los endpoints están documentados  
✅ El servidor reinicia automáticamente al cambiar código  
✅ Usa `curl` para probar desde terminal  
✅ Revisa `server.log` si hay errores  

---

## ✨ ¿Qué Sigue?

**Opción A (Fácil):** Abre http://localhost:8000/docs y juega con los endpoints

**Opción B (Intermedio):** Ejecuta ejemplos: `python examples.py`

**Opción C (Avanzado):** Modifica el código en `src/main.py` y verás cambios en vivo

---

**¡El proyecto está 100% operacional! 🎉**

Fecha: 2026-01-22  
Servidor: ACTIVO ✅  
Documentación: DISPONIBLE ✅  
Ejemplos: LISTOS ✅
