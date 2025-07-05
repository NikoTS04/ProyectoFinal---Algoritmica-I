# config.py
"""
Configuración global del analizador de complejidad temporal
"""

import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
EJEMPLOS_DIR = PROJECT_ROOT / "ejemplos"
ANALISIS_DIR = PROJECT_ROOT / "analisis_guardados"

# Configuración de matplotlib
MATPLOTLIB_BACKEND = 'TkAgg'
MATPLOTLIB_DPI = 100

# Configuración de la interfaz
VENTANA_ANCHO = 900
VENTANA_ALTO = 700
VENTANA_MINIMO_ANCHO = 800
VENTANA_MINIMO_ALTO = 600
TEMA_GUI = "flatly"

# Configuración del análisis
RANGO_GRAFICA_DEFAULT = (1, 20)
EXTENSION_ANALISIS = ".json"

# Crear directorios si no existen
def inicializar_directorios():
    """Crea los directorios necesarios si no existen"""
    ANALISIS_DIR.mkdir(exist_ok=True)
    EJEMPLOS_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    inicializar_directorios()
    print("Directorios inicializados correctamente")
