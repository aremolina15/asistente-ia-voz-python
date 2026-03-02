#!/bin/bash

# Script para iniciar el cliente de voz DevOps
# Uso: ./start_voice_client.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( dirname "$SCRIPT_DIR" )"

echo "🚀 Iniciando Cliente de Voz DevOps"
echo "=================================="
echo ""

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ No se encontró entorno virtual (.venv o venv)"
    exit 1
fi

# Exportar variables de entorno (si existe .env)
if [ -f ".env" ]; then
    echo "🔐 Cargando variables desde .env..."
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
if ! curl -fs http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo "⚠️  El servidor no está corriendo en 127.0.0.1:8000"
    echo ""
    echo "Por favor, inicia el servidor en otra terminal con:"
    echo "  cd '$PROJECT_DIR'"
    echo "  source .venv/bin/activate  # o source venv/bin/activate"
    echo "  python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload"
    echo ""
    exit 1
fi
echo "✅ Servidor OK"

# Verificar credenciales opcionales
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ] && [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "⚠️  GOOGLE_APPLICATION_CREDENTIALS apunta a un archivo inexistente"
    echo "   $GOOGLE_APPLICATION_CREDENTIALS"
fi

echo ""
echo "=================================="
echo "✅ Todo listo. Iniciando cliente..."
echo "=================================="
echo ""

# Iniciar cliente de voz
python voice_client.py

# Cleanup
trap "echo 'Limpiando...'; pkill -f 'ffplay' || true; exit 0" EXIT
