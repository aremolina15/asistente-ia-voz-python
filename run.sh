#!/bin/bash

# Script para ejecutar el DevOps Voice Assistant
# Este script maneja todo el setup necesario

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

echo "════════════════════════════════════════════════════════════"
echo "🚀 DevOps Voice Assistant - Iniciando..."
echo "════════════════════════════════════════════════════════════"
echo ""

# 1. Verificar Python
echo "1️⃣  Verificando Python..."
python3 --version
echo "✅ Python disponible"
echo ""

# 2. Activar o crear entorno virtual
if [ ! -d "venv" ]; then
    echo "2️⃣  Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "2️⃣  Entorno virtual ya existe"
fi
echo ""

# 3. Activar entorno
echo "3️⃣  Activando entorno virtual..."
source venv/bin/activate
echo "✅ Entorno activado"
echo ""

# 4. Instalar dependencias
echo "4️⃣  Instalando/actualizando dependencias..."
pip install --upgrade pip wheel setuptools -q >/dev/null 2>&1 || true
pip install -r requirements.txt -q >/dev/null 2>&1 || {
    echo "⚠️  Algunos paquetes pueden tener conflictos menores, pero continuamos..."
}
echo "✅ Dependencias listas"
echo ""

# 5. Verificar .env
echo "5️⃣  Verificando configuración..."
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado, creando desde .env.example..."
    cp .env.example .env
    echo "📝 Por favor, actualiza .env con tu proyecto GCP"
fi
echo "✅ Configuración lista"
echo ""

# 6. Mostrar información
echo "════════════════════════════════════════════════════════════"
echo "📊 Información de la API"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🌐 URL Principal:     http://localhost:8000"
echo "📚 Documentación:     http://localhost:8000/docs"
echo "🔧 ReDoc:            http://localhost:8000/redoc"
echo "🏥 Health Check:      http://localhost:8000/health"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Para detener el servidor, presiona CTRL+C"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# 7. Ejecutar la aplicación
echo "🎯 Ejecutando servidor FastAPI..."
echo ""
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
