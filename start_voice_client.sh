#!/bin/bash

# Script para iniciar el cliente de voz DevOps
# Uso: ./start_voice_client.sh

set -e

# Usar el directorio actual o especificar via variable de entorno
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"

echo "🚀 Iniciando Cliente de Voz DevOps"
echo "=================================="
echo ""

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Cargar variables de entorno desde .env si existe
if [ -f .env ]; then
    echo "🔐 Cargando configuración desde .env..."
    # Usar set -a para exportar automáticamente las variables
    set -a
    source .env
    set +a
else
    echo "⚠️  Archivo .env no encontrado. Usando variables de entorno del sistema..."
fi

# Verificar que las variables requeridas estén configuradas
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ GOOGLE_APPLICATION_CREDENTIALS no está configurado"
    echo "   Por favor, exporta la variable o agrégala al archivo .env"
    exit 1
fi

if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "❌ GOOGLE_CLOUD_PROJECT no está configurado"
    echo "   Por favor, exporta la variable o agrégala al archivo .env"
    exit 1
fi

echo "✅ Configuración cargada"

# Verificar que el servidor esté corriendo
echo "🔍 Verificando servidor..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  El servidor no está corriendo en localhost:8000"
    echo ""
    echo "Por favor, inicia el servidor en otra terminal con:"
    echo "  cd \$PROJECT_DIR"
    echo "  source venv/bin/activate"
    echo "  python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
    echo ""
    exit 1
fi
echo "✅ Servidor OK"

# Verificar credenciales
if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ Archivo de credenciales no encontrado:"
    echo "   $GOOGLE_APPLICATION_CREDENTIALS"
    exit 1
fi
echo "✅ Credenciales OK"

echo ""
echo "=================================="
echo "✅ Todo listo. Iniciando cliente..."
echo "=================================="
echo ""

# Iniciar cliente de voz
python voice_client.py

# Cleanup
trap "echo 'Limpiando...'; pkill -f 'ffplay' || true; exit 0" EXIT
