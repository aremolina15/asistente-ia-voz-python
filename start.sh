#!/bin/bash

# Script rápido para ejecutar el servidor

# Usar el directorio actual o especificar via variable de entorno
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"

cd "$PROJECT_DIR"

echo "═════════════════════════════════════════════════════════════"
echo "🚀 Iniciando DevOps Voice Assistant"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Activar entorno
source venv/bin/activate

# Instalar paquetes mínimos
echo "📦 Instalando paquetes necesarios..."
pip install -q fastapi uvicorn pydantic python-dotenv 2>/dev/null || true

echo ""
echo "✅ Listo!"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo "📊 Información de la API"
echo "═════════════════════════════════════════════════════════════"
echo ""
echo "  🌐 API Principal:    http://localhost:8000"
echo "  📚 Documentación:    http://localhost:8000/docs"
echo "  🏥 Health Check:     curl http://localhost:8000/health"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""

# Ejecutar servidor
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
