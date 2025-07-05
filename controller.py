#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo básico de uso del analizador de complejidad
================================================

Este archivo muestra cómo usar el analizador desde código.
Para la interfaz gráfica, use main.py
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.pseudogrammar import tokenizar
from core.parser_estructural import parsear
from core.analizador_complejidad import AnalizadorComplejidad

codigo = '''
Funcion ejemplo(N)
    x <- a + b * c
    Para i desde 2 hasta N+1 hacer
        x <- x + i
    fPara
fFuncion
'''

print("Ejemplo básico de análisis:")
print("Código:")
print(codigo)

tokens = tokenizar(codigo)
arbol = parsear(tokens)
analizador = AnalizadorComplejidad(arbol)
resultado = analizador.analizar('ejemplo')

print("\nResultado:")
resultado.mostrar()

# Opcional: mostrar gráfica
try:
    print("\nGenerando gráfica...")
    resultado.graficar(rango=(1, 20))
except Exception as e:
    print(f"No se pudo mostrar la gráfica: {e}")
    print("Use la interfaz gráfica (main.py) para visualización.")