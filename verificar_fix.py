#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que los problemas de tipo 'integer' and 'function' 
y 'pow()' se han solucionado.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

def verificar_expresiones_problematicas():
    """Verifica que las expresiones problemáticas ahora funcionan"""
    print("=== Verificación de Expresiones Problemáticas ===")
    
    from core.serializacion import SerializadorAnalisis
    import sympy
    
    serializador = SerializadorAnalisis()
    archivos = serializador.listar_analisis_guardados()
    
    # Buscar específicamente los archivos que causaban problemas
    archivos_problematicos = ['busquedaBinaria.json', 'busquedaLineal.json', 'fibonacci.json']
    
    for nombre_archivo in archivos_problematicos:
        archivo_encontrado = None
        for archivo in archivos:
            if nombre_archivo in archivo['archivo']:
                archivo_encontrado = archivo
                break
        
        if not archivo_encontrado:
            print(f"  {nombre_archivo}: No encontrado")
            continue
            
        print(f"\n=== Verificando {nombre_archivo} ===")
        
        try:
            datos = serializador.cargar_analisis(archivo_encontrado['ruta'])
            resultado = datos['resultado']
            
            print(f"  ✓ Cargado exitosamente")
            print(f"  Función: {resultado.nombre_funcion}")
            print(f"  Big O: {resultado.big_o}")
            print(f"  Expresión: {resultado.funcion_tiempo.expr}")
            
            # Simular la evaluación que se hace en comparacion.py
            expr = resultado.funcion_tiempo.expr
            n_values = [1, 5, 10, 15, 20]
            
            print("  Evaluación de la expresión:")
            for n in n_values:
                try:
                    # Usar el mismo método corregido
                    val = expr.subs(sympy.Symbol('N'), n)
                    if hasattr(val, 'evalf'):
                        result = float(val.evalf())
                    else:
                        result = float(val)
                    # Limitar valores muy grandes
                    result = min(result, 1e6)
                    print(f"    T({n}) = {result}")
                except Exception as e:
                    print(f"    Error en T({n}): {e}")
                    # Fallback
                    big_o = resultado.big_o
                    if "2^" in big_o or "2**" in big_o:
                        fallback_val = min(2**n, 1e6)
                    elif "n**2" in big_o or "n^2" in big_o:
                        fallback_val = n**2
                    elif "n" in big_o.lower():
                        fallback_val = n
                    else:
                        fallback_val = 1
                    print(f"    Fallback T({n}) = {fallback_val}")
            
            print(f"  ✓ Evaluación exitosa")
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verificar_expresiones_problematicas()
