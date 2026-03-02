#!/usr/bin/env python3
"""
Script para mostrar la estructura del proyecto
"""

import os
from pathlib import Path

def create_tree(directory, prefix="", exclude_dirs={".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules", ".env"}):
    """Crear árbol de directorios"""
    contents = []
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        return contents
    
    # Filtrar items
    items = [item for item in items if item not in exclude_dirs and not item.startswith('.')]
    
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        contents.append(f"{prefix}{current_prefix}{item}")
        
        if os.path.isdir(path) and not item.startswith('.'):
            next_prefix = prefix + ("    " if is_last else "│   ")
            contents.extend(create_tree(path, next_prefix, exclude_dirs))
    
    return contents

def main():
    project_root = Path(__file__).resolve().parent.parent
    
    print("📁 Estructura del Proyecto - DevOps Voice Assistant")
    print("=" * 60)
    print()
    print(f"Raíz: {project_root}")
    print()
    print("asistente-ia-voz-python/")
    
    tree_lines = create_tree(str(project_root))
    for line in tree_lines:
        print(line)
    
    print()
    print("=" * 60)
    print()
    print("📊 Resumen:")
    print()
    
    # Contar archivos
    py_files = 0
    test_files = 0
    doc_files = 0
    config_files = 0
    
    for root, dirs, files in os.walk(project_root):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "venv", "__pycache__"}]
        
        for file in files:
            if file.endswith(".py"):
                py_files += 1
                if "test" in file:
                    test_files += 1
            elif file.endswith((".md", ".txt")):
                doc_files += 1
            elif file in {"Dockerfile", "docker-compose.yml", ".env.example", "requirements.txt", ".gitignore"}:
                config_files += 1
    
    print(f"🐍 Archivos Python: {py_files}")
    print(f"🧪 Archivos de Test: {test_files}")
    print(f"📚 Documentación: {doc_files}")
    print(f"⚙️ Configuración: {config_files}")
    print()
    print("🎯 Módulos Principales:")
    print("  • src/main.py - Punto de entrada FastAPI")
    print("  • src/services/ - Lógica de negocio (GCP, Gobernanza, IA)")
    print("  • src/routers/ - Endpoints API")
    print("  • tests/ - Tests unitarios")
    print("  • deployment/ - Configuración Docker y Kubernetes")
    print()

if __name__ == "__main__":
    main()
