#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que la comparación funciona correctamente
con análisis guardados.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

def test_cargar_analisis():
    """Prueba cargar análisis guardados"""
    print("=== Prueba de Carga de Análisis ===")
    
    from core.serializacion import SerializadorAnalisis
    import sympy
    
    serializador = SerializadorAnalisis()
    archivos = serializador.listar_analisis_guardados()
    
    print(f"Archivos encontrados: {len(archivos)}")
    
    for archivo in archivos[:3]:  # Probar solo los primeros 3
        print(f"\nProbando: {archivo['archivo']}")
        try:
            datos = serializador.cargar_analisis(archivo['ruta'])
            resultado = datos['resultado']
            
            print(f"  Función: {resultado.nombre_funcion}")
            print(f"  Big O: {resultado.big_o}")
            print(f"  Expresión: {resultado.funcion_tiempo.expr}")
            
            # Probar evaluación
            expr = resultado.funcion_tiempo.expr
            for n in [1, 5, 10]:
                try:
                    val = expr.subs(sympy.Symbol('N'), n)
                    if hasattr(val, 'evalf'):
                        result = float(val.evalf())
                    else:
                        result = float(val)
                    print(f"  T({n}) = {result}")
                except Exception as e:
                    print(f"  Error evaluando T({n}): {e}")
                    
        except Exception as e:
            print(f"  Error cargando: {e}")

if __name__ == "__main__":
    test_cargar_analisis()
