#!/bin/bash

# Script de setup para DevOps Voice Assistant
# Uso: ./setup.sh <project-id>

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Validar argumentos
if [ -z "$1" ]; then
    print_error "Project ID es requerido"
    echo "Uso: ./setup.sh <project-id>"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-us-central1}

print_info "Configurando DevOps Voice Assistant para proyecto: $PROJECT_ID"

# 1. Verificar gcloud CLI
print_info "Verificando gcloud CLI..."
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI no está instalado"
    exit 1
fi
print_success "gcloud CLI verificado"

# 2. Autenticar con GCP
print_info "Autenticando con GCP..."
gcloud auth login

# 3. Configurar proyecto
print_info "Configurando proyecto $PROJECT_ID..."
gcloud config set project $PROJECT_ID
print_success "Proyecto configurado"

# 4. Habilitar APIs requeridas
print_info "Habilitando APIs requeridas..."
gcloud services enable \
    speech.googleapis.com \
    texttospeech.googleapis.com \
    aiplatform.googleapis.com \
    storage.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    container.googleapis.com
print_success "APIs habilitadas"

# 5. Crear bucket de storage
BUCKET_NAME="devops-voice-assistant-${PROJECT_ID}"
print_info "Creando bucket: $BUCKET_NAME..."
if ! gsutil ls -b gs://$BUCKET_NAME &> /dev/null; then
    gsutil mb -l $REGION gs://$BUCKET_NAME
    print_success "Bucket creado"
else
    print_success "Bucket ya existe"
fi

# 6. Crear archivo .env
print_info "Creando archivo .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    sed -i "s/tu-proyecto-gcp/$PROJECT_ID/" .env
    sed -i "s/us-central1/$REGION/" .env
    sed -i "s/devops-assistant-storage/$BUCKET_NAME/" .env
    print_success ".env creado"
else
    print_info ".env ya existe, saltando"
fi

# 7. Crear entorno virtual
print_info "Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Entorno virtual creado"
else
    print_success "Entorno virtual ya existe"
fi

# 8. Instalar dependencias
print_info "Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencias instaladas"

# 9. Setup autenticación de aplicación default
print_info "Configurando Application Default Credentials..."
gcloud auth application-default login

print_success "✨ Setup completado exitosamente!"
print_info "Próximos pasos:"
echo "1. Actualiza .env con tus configuraciones específicas"
echo "2. Ejecuta: source venv/bin/activate"
echo "3. Ejecuta: python -m uvicorn src.main:app --reload"
echo "4. Accede a http://localhost:8000/docs"
