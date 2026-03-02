# Guía de Seguridad

## 🔒 Configuración Segura

### 1. Variables de Entorno

**NUNCA** incluyas credenciales o información sensible directamente en el código. Usa variables de entorno:

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env con tus valores reales
# IMPORTANTE: .env está en .gitignore y NO debe ser commiteado
```

### 2. Credenciales de GCP

Las credenciales de Google Cloud **NUNCA** deben ser commiteadas al repositorio:

```bash
# ✅ CORRECTO: Usar variable de entorno
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/segura/a/credenciales.json"

# ❌ INCORRECTO: Hardcodear en el código
# GOOGLE_APPLICATION_CREDENTIALS = "/home/usuario/credenciales.json"
```

**Nota**: El archivo `.gitignore` ya está configurado para excluir archivos `.json` excepto `requirements.json`.

### 3. SECRET_KEY

En producción, **SIEMPRE** usa una clave secreta única y segura:

```bash
# Generar una clave secreta segura
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Agregar al archivo .env
SECRET_KEY=tu-clave-generada-aqui
```

### 4. CORS (Cross-Origin Resource Sharing)

En producción, configura dominios específicos en lugar de permitir todos:

```bash
# En .env
ALLOWED_ORIGINS=https://tudominio.com,https://app.tudominio.com
```

### 5. ID del Proyecto GCP

Usa variables de entorno en lugar de hardcodear tu ID de proyecto:

```bash
# En .env
GOOGLE_CLOUD_PROJECT=tu-proyecto-gcp
```

## 🛡️ Mejores Prácticas

### Antes de Commitear

1. **Revisa** que no haya credenciales en el código
2. **Verifica** que los archivos sensibles estén en `.gitignore`
3. **Usa** `git diff` para revisar los cambios antes de commit
4. **Ejecuta** `git status` para ver qué archivos serán incluidos

### Archivos que NUNCA deben ser commiteados

- ✋ Archivos `.env` (excepto `.env.example`)
- ✋ Credenciales JSON de GCP
- ✋ Claves API o tokens
- ✋ Información personal (nombres de usuario, rutas de sistema)
- ✋ Contraseñas o secretos

### Si Accidentalmente Commiteas Información Sensible

1. **NO** intentes simplemente eliminar el archivo en un nuevo commit
2. **Revoca** inmediatamente cualquier credencial expuesta
3. **Contacta** al administrador del repositorio
4. **Considera** usar herramientas como `git-filter-repo` para limpiar el historial

## 📋 Checklist de Seguridad

Antes de desplegar a producción:

- [ ] Todas las credenciales están en variables de entorno
- [ ] `SECRET_KEY` tiene un valor único y seguro
- [ ] `ALLOWED_ORIGINS` está configurado con dominios específicos
- [ ] `DEBUG=False` en producción
- [ ] Las credenciales de GCP tienen permisos mínimos necesarios
- [ ] Cloud Audit Logs está habilitado
- [ ] Se usa HTTPS para todas las comunicaciones
- [ ] Los buckets de Storage tienen control de acceso apropiado

## 🚨 Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad, por favor:

1. **NO** abras un issue público
2. Contacta directamente al mantenedor del proyecto
3. Proporciona detalles específicos de la vulnerabilidad
4. Permite tiempo razonable para una solución antes de divulgación pública

## 📚 Referencias

- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
