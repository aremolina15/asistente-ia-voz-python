# Contribuyendo al Proyecto

Primero, ¡gracias por tu interés en contribuir! 🎉

## Cómo Contribuir

### Reportar Bugs
1. Verifica que el bug no haya sido reportado en [Issues](https://github.com/aremolina15/asistente-ia-voz-python/issues)
2. Si es nuevo, crea un issue con:
   - Título descriptivo
   - Descripción detallada
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Tu entorno (Python version, OS, etc)

### Sugerir Mejoras
1. Usa la etiqueta `enhancement` en Issues
2. Describe el problema que resuelve
3. Ejemplos de la mejora
4. Beneficios potenciales

### Enviar Pull Requests

#### 1. Fork y Clonar
```bash
git clone https://github.com/tu-usuario/asistente-ia-voz-python.git
cd asistente-ia-voz-python
git remote add upstream https://github.com/aremolina15/asistente-ia-voz-python.git
```

#### 2. Crear Rama
```bash
git checkout -b feature/my-amazing-feature
# o
git checkout -b bugfix/issue-description
```

#### 3. Hacer Cambios
- Mantén la consistencia de código
- Escribe tests para nuevas funcionalidades
- Actualiza documentación si es necesario

#### 4. Tests y Linting
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/ -v --cov=src

# Formatear código
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
mypy src/
```

#### 5. Commit
```bash
# Mensajes descriptivos siguiendo: <tipo>: <descripción>
# Tipos: feat, fix, docs, style, refactor, test, chore

git commit -m "feat: add voice analysis for new infrastructure types"
```

#### 6. Push y PR
```bash
git push origin feature/my-amazing-feature
```
Luego crea un Pull Request en GitHub con:
- Descripción clara del cambio
- Referencia a issue relacionado (#123)
- Screenshots/ejemplos si aplica

## Guías de Estilo

### Python
- Seguir PEP 8
- Type hints en funciones
- Docstrings en módulos/clases/funciones

```python
def analyze_governance(
    resource_type: str,
    resource_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analizar gobernanza de un recurso.
    
    Args:
        resource_type: Tipo de recurso (iam, storage, gke)
        resource_data: Datos del recurso a analizar
        
    Returns:
        Análisis de gobernanza con findings y score
    """
    pass
```

### Documentación
- Markdown bien formateado
- Enlaces funcionales
- Ejemplos ejecutables
- Actualizaciones de README si es necesario

### Commits
- Mensajes claros y descriptivos
- Commits pequeños y enfocados
- Referencia a issues: `Fixes #123`

## Estructura de Directorios

```
src/
├── main.py                    # Punto de entrada
├── config.py                  # Configuración
├── models/                    # Modelos de datos
├── services/                  # Lógica de negocio
├── routers/                   # Endpoints API
├── schemas/                   # Schemas de Pydantic
└── utils/                     # Utilidades

tests/
├── test_governance.py         # Tests de gobernanza
├── test_voice.py              # Tests de voz
└── test_ai_service.py         # Tests de IA

deployment/
├── Dockerfile
├── docker-compose.yml
└── k8s/                       # Manifiestos Kubernetes
```

## Áreas de Contribución Prioritarias

- [ ] Análisis de Terraform
- [ ] Integración con Cloud Monitoring
- [ ] Support para multiple clouds (AWS, Azure)
- [ ] CLI mejorada
- [ ] Documentación en otros idiomas
- [ ] Casos de uso adicionales

## Criterios de Aceptación

Los PRs serán aceptados si:
- [ ] Pasan todos los tests
- [ ] Mantienen cobertura de código >80%
- [ ] Siguen las guías de estilo
- [ ] Incluyen documentación
- [ ] Al menos 1 review positivo

## Configurar Ambiente de Desarrollo

```bash
# Clone y setup
git clone https://github.com/tu-usuario/asistente-ia-voz-python.git
cd asistente-ia-voz-python

# Crear entorno
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar con dev dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

## Ejecutar Localmente

```bash
# Desarrollo
python -m uvicorn src.main:app --reload

# Testing
pytest tests/ -v --cov=src

# Linting completo
make lint  # Si existe Makefile
```

## Preguntas?

- 📧 Email: [tu-email]
- 💬 Discussions: GitHub Discussions
- 📚 Documentación: Ver [ARCHITECTURE.md](ARCHITECTURE.md)

## Código de Conducta

Se espera que todos los contribuidores:
- Sean respetuosos y profesionales
- Acepten críticas constructivas
- Se enfoquen en lo mejor para el proyecto
- Reporten comportamiento inadecuado

---

¡Gracias por ayudar a mejorar este proyecto! 🚀
