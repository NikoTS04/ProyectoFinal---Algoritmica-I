#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de limpieza para eliminar archivos temporales y de debug.
Ejecutar antes de hacer commit a GitHub.
"""

import os
import glob
import shutil
from pathlib import Path

def limpiar_archivos_temporales():
    """Elimina archivos temporales y de debug"""
    
    # Directorio base del proyecto
    base_dir = Path(__file__).parent
    
    print("🧹 Limpiando archivos temporales...")
    
    # Patrones de archivos a eliminar
    patrones_archivos = [
        "debug_*.py",
        "test_*.py", 
        "temp_*.py",
        "prueba_*.py",
        "verificar_*.py",
        "ejemplo_*.txt",  # Solo en la raíz, no en ejemplos/
        "config.py",
        "*.tmp",
        "*.pyc",
    ]
    
    # Directorios a limpiar recursivamente
    patrones_directorios = [
        "__pycache__",
        "*.egg-info",
        ".pytest_cache",
    ]
    
    archivos_eliminados = 0
    directorios_eliminados = 0
    
    # Eliminar archivos temporales
    for patron in patrones_archivos:
        archivos = list(base_dir.glob(patron))
        for archivo in archivos:
            # No eliminar ejemplos de la carpeta ejemplos/
            if "ejemplo_" in archivo.name and "ejemplos" in str(archivo.parent):
                continue
            try:
                archivo.unlink()
                print(f"  ✓ Eliminado: {archivo.name}")
                archivos_eliminados += 1
            except Exception as e:
                print(f"  ✗ Error eliminando {archivo.name}: {e}")
    
    # Eliminar directorios temporales
    for patron in patrones_directorios:
        directorios = list(base_dir.rglob(patron))
        for directorio in directorios:
            try:
                shutil.rmtree(directorio)
                print(f"  ✓ Directorio eliminado: {directorio}")
                directorios_eliminados += 1
            except Exception as e:
                print(f"  ✗ Error eliminando {directorio}: {e}")
    
    # Limpiar análisis temporales con timestamp
    analisis_dir = base_dir / "analisis_guardados"
    if analisis_dir.exists():
        for archivo in analisis_dir.glob("analisis_20*.json"):
            try:
                archivo.unlink()
                print(f"  ✓ Análisis temporal eliminado: {archivo.name}")
                archivos_eliminados += 1
            except Exception as e:
                print(f"  ✗ Error eliminando {archivo.name}: {e}")
    
    print(f"\n✅ Limpieza completada:")
    print(f"   📄 Archivos eliminados: {archivos_eliminados}")
    print(f"   📁 Directorios eliminados: {directorios_eliminados}")
    
    return archivos_eliminados + directorios_eliminados > 0

def verificar_estructura():
    """Verifica que la estructura del proyecto esté limpia"""
    base_dir = Path(__file__).parent
    
    print("\n🔍 Verificando estructura del proyecto...")
    
    # Archivos que deben existir
    archivos_requeridos = [
        "main.py",
        "README.md", 
        "requirements.txt",
        ".gitignore",
        "src/core/analizador_complejidad.py",
        "src/core/expresion_simbolica.py",
        "ejemplos/README.md",
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not (base_dir / archivo).exists():
            faltantes.append(archivo)
    
    if faltantes:
        print("  ⚠️  Archivos faltantes:")
        for archivo in faltantes:
            print(f"    - {archivo}")
    else:
        print("  ✅ Todos los archivos requeridos están presentes")
    
    # Verificar que no haya archivos temporales
    temporales = []
    for patron in ["debug_*.py", "test_*.py", "temp_*.py"]:
        temporales.extend(base_dir.glob(patron))
    
    if temporales:
        print("  ⚠️  Archivos temporales encontrados:")
        for archivo in temporales:
            print(f"    - {archivo}")
        return False
    else:
        print("  ✅ No se encontraron archivos temporales")
        return True

if __name__ == "__main__":
    print("🚀 SCRIPT DE LIMPIEZA DEL PROYECTO")
    print("=" * 50)
    
    limpio = limpiar_archivos_temporales()
    estructura_ok = verificar_estructura()
    
    print("\n" + "=" * 50)
    if estructura_ok:
        print("✅ Proyecto listo para commit!")
    else:
        print("⚠️  Revise los problemas antes de hacer commit")
