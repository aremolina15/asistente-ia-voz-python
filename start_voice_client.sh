#!/bin/bash

# Script para iniciar el cliente de voz DevOps
# Uso: ./start_voice_client.sh

set -e

PROJECT_DIR="/home/aremol1/Documents/LABs Personal/IA-VOZ-DEVOPS/asistente-ia-voz-python"

echo "🚀 Iniciando Cliente de Voz DevOps"
echo "=================================="
echo ""

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Exportar variables de entorno
echo "🔐 Configurando credenciales GCP..."
export GOOGLE_APPLICATION_CREDENTIALS="/home/aremol1/Documents/LABs Personal/IA-VOZ-DEVOPS/application_default_credentials.json"
export GOOGLE_CLOUD_PROJECT="heroic-dolphin-455016-q8"

# Verificar que el servidor esté corriendo
echo "🔍 Verificando servidor..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  El servidor no está corriendo en localhost:8000"
    echo ""
    echo "Por favor, inicia el servidor en otra terminal con:"
    echo "  cd '$PROJECT_DIR'"
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
