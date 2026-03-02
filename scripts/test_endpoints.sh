#!/bin/bash

# Script para probar los endpoints de voz sin micrófono

API="http://localhost:8000/api/v1/voice"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( dirname "$SCRIPT_DIR" )"
TMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cd "$PROJECT_DIR"

echo "🧪 Pruebas de Endpoint de Voz"
echo "=============================="
echo ""

# Test 1: Health check
echo "1️⃣ Verificando servidor..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ Servidor activo"
else
    echo "❌ Servidor no responde"
    exit 1
fi

echo ""
echo "2️⃣ Probando endpoint /synthesize..."

# Test 2: Synthesize - texto a voz
TEXT_QUERY='{"text": "Hola, soy tu asistente de DevOps. ¿En qué puedo ayudarte?", "language_code": "es-ES"}'

RESPONSE=$(curl -s -X POST "$API/synthesize" \
    -H "Content-Type: application/json" \
    -d "$TEXT_QUERY")

if echo "$RESPONSE" | grep -q "audio_base64"; then
    echo "✅ Síntesis de voz funcionando"
    echo "   Extrayendo audio base64..."
    
    # Decodificar y guardar el MP3
    AUDIO_B64=$(echo "$RESPONSE" | grep -o '"audio_base64":"[^"]*"' | cut -d'"' -f4)
    echo "$AUDIO_B64" | base64 -d > "$TMP_DIR/test_audio.mp3"
    
    if [ -f "$TMP_DIR/test_audio.mp3" ]; then
        SIZE=$(ls -lh "$TMP_DIR/test_audio.mp3" | awk '{print $5}')
        echo "   📁 Audio guardado temporalmente: $TMP_DIR/test_audio.mp3 ($SIZE)"
        echo "   Intentando reproducir..."
        ffplay -nodisp -autoexit "$TMP_DIR/test_audio.mp3" 2>/dev/null
    fi
else
    echo "❌ Error en síntesis de voz"
    echo "Respuesta: $RESPONSE"
fi

echo ""
echo "3️⃣ Probando endpoint /query..."

# Test 3: Query - consulta a IA + respuesta de voz
QUERY='{"query": "¿Cómo despliego una aplicación en GCP?", "language_code": "es-ES"}'

QUERY_RESPONSE=$(curl -s -X POST "$API/query" \
    -H "Content-Type: application/json" \
    -d "$QUERY")

if echo "$QUERY_RESPONSE" | grep -q "response"; then
    echo "✅ Consulta a IA funcionando"
    
    # Extraer respuesta
    AI_RESPONSE=$(echo "$QUERY_RESPONSE" | grep -o '"response":"[^"]*"' | cut -d'"' -f4 | head -c 100)
    echo "   🤖 Respuesta: ${AI_RESPONSE}..."
    
    # Guardar audio
    if echo "$QUERY_RESPONSE" | grep -q "audio_base64"; then
        AUDIO_B64=$(echo "$QUERY_RESPONSE" | grep -o '"audio_base64":"[^"]*"' | cut -d'"' -f4)
        echo "$AUDIO_B64" | base64 -d > "$TMP_DIR/query_response.mp3"
        
        if [ -f "$TMP_DIR/query_response.mp3" ]; then
            SIZE=$(ls -lh "$TMP_DIR/query_response.mp3" | awk '{print $5}')
            echo "   📁 Audio respuesta temporal: $TMP_DIR/query_response.mp3 ($SIZE)"
        fi
    fi
else
    echo "❌ Error en consulta a IA"
    echo "Respuesta: $QUERY_RESPONSE"
fi

echo ""
echo "=============================="
echo "✅ Pruebas completadas"
echo ""
echo "Próximos pasos:"
echo "1. Ejecuta: python voice_client.py"
echo "2. Habla tu pregunta"
echo "3. Espera 2.5s de silencio"
echo "4. La IA responderá automáticamente"
