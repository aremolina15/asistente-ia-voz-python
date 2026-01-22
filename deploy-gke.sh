#!/bin/bash

# Script para desplegar en GKE
# Uso: ./deploy-gke.sh <project-id> <cluster-name> <region>

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

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
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    print_error "Argumentos requeridos"
    echo "Uso: ./deploy-gke.sh <project-id> <cluster-name> <region>"
    exit 1
fi

PROJECT_ID=$1
CLUSTER_NAME=$2
REGION=$3
REGISTRY="gcr.io/$PROJECT_ID"
IMAGE_NAME="devops-voice-assistant"
IMAGE_TAG="latest"

print_info "Desplegando en GKE: $CLUSTER_NAME ($REGION)"

# 1. Configurar gcloud
print_info "Configurando gcloud..."
gcloud config set project $PROJECT_ID
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# 2. Construir imagen Docker
print_info "Construyendo imagen Docker..."
docker build -t $REGISTRY/$IMAGE_NAME:$IMAGE_TAG .
print_success "Imagen construida"

# 3. Pushear imagen a Container Registry
print_info "Pusheando imagen a Container Registry..."
docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
print_success "Imagen pusheada"

# 4. Crear namespace
print_info "Creando namespace..."
kubectl create namespace devops --dry-run=client -o yaml | kubectl apply -f -

# 5. Crear ConfigMap
print_info "Creando ConfigMap..."
kubectl create configmap devops-voice-config \
    --from-literal=project_id=$PROJECT_ID \
    --from-literal=region=$REGION \
    --from-literal=log_level=INFO \
    --from-literal=storage_bucket=devops-voice-assistant-$PROJECT_ID \
    -n devops \
    --dry-run=client -o yaml | kubectl apply -f -

# 6. Crear ServiceAccount
print_info "Creando ServiceAccount..."
kubectl create serviceaccount devops-voice-assistant -n devops --dry-run=client -o yaml | kubectl apply -f -

# 7. Actualizar imagen en deployment
print_info "Actualizando imagen en Deployment..."
sed -i "s|gcr.io/PROJECT_ID/devops-voice-assistant:latest|$REGISTRY/$IMAGE_NAME:$IMAGE_TAG|g" deployment/k8s/deployment.yaml

# 8. Desplegar
print_info "Desplegando..."
kubectl apply -f deployment/k8s/

# 9. Esperar rollout
print_info "Esperando rollout..."
kubectl rollout status deployment/devops-voice-assistant -n devops --timeout=300s
print_success "Rollout completado"

# 10. Mostrar info del servicio
print_success "Despliegue completado!"
print_info "Información del servicio:"
kubectl get svc -n devops
kubectl get pods -n devops
