.PHONY: help setup install install-dev run dev test coverage lint format docker-build docker-up docker-down clean

help:
	@echo "DevOps Voice Assistant - Tareas Disponibles"
	@echo ""
	@echo "Setup:"
	@echo "  make setup GCP_PROJECT=<project-id>  Configurar el proyecto"
	@echo "  make install                         Instalar dependencias"
	@echo "  make install-dev                     Instalar dependencias de desarrollo"
	@echo ""
	@echo "Desarrollo:"
	@echo "  make run                             Ejecutar la aplicación"
	@echo "  make dev                             Ejecutar en modo desarrollo"
	@echo ""
	@echo "Testing:"
	@echo "  make test                            Ejecutar tests"
	@echo "  make coverage                        Reporte de cobertura"
	@echo ""
	@echo "Calidad de Código:"
	@echo "  make lint                            Ejecutar linters"
	@echo "  make format                          Formatear código"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build                    Construir imagen Docker"
	@echo "  make docker-up                       Iniciar contenedores"
	@echo "  make docker-down                     Detener contenedores"
	@echo ""
	@echo "Utilidades:"
	@echo "  make clean                           Limpiar archivos temporales"
	@echo "  make show-structure                  Mostrar estructura del proyecto"
	@echo "  make examples                        Ejecutar ejemplos de API"

# Setup
setup:
	@if [ -z "$(GCP_PROJECT)" ]; then \
		echo "❌ Error: Debes proporcionar GCP_PROJECT"; \
		echo "Uso: make setup GCP_PROJECT=your-project-id"; \
		exit 1; \
	fi
	chmod +x scripts/setup.sh
	./scripts/setup.sh $(GCP_PROJECT)

# Instalación
install:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

install-dev: install
	. venv/bin/activate && pip install -r requirements-dev.txt

# Desarrollo
run:
	python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

dev:
	python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	pytest tests/ -v

coverage:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "📊 Reporte HTML generado en: htmlcov/index.html"

# Linting y Formato
lint:
	@echo "🔍 Ejecutando flake8..."
	flake8 src/ tests/
	@echo "🔍 Ejecutando mypy..."
	mypy src/
	@echo "✅ Linting completado"

format:
	@echo "🎨 Formateando código con Black..."
	black src/ tests/
	@echo "🎨 Organizando imports con isort..."
	isort src/ tests/
	@echo "✅ Formateo completado"

# Docker
docker-build:
	docker build -t devops-voice-assistant:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

# Utilidades
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✅ Limpieza completada"

show-structure:
	python scripts/show-structure.py

examples:
	python examples/api_examples.py

# Tareas combinadas
check: lint test coverage
	@echo "✅ Todas las comprobaciones pasaron"

all: install-dev lint test docker-build
	@echo "✅ Build completado"

.DEFAULT_GOAL := help
