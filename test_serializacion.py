#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la serialización corregida
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.pseudogrammar import tokenizar
from core.parser_estructural import parsear
from core.analizador_complejidad import AnalizadorComplejidad
from core.serializacion import SerializadorAnalisis

def probar_serializacion():
    # Ejemplo simple
    codigo = '''
Funcion ejemplo(N)
    Para i desde 1 hasta N hacer
        x <- x + 1
    fPara
fFuncion
'''
    
    print("=== Probando Serialización ===")
    print(f"Código:\n{codigo}")
    
    # Análisis
    tokens = tokenizar(codigo)
    arbol = parsear(tokens)
    analizador = AnalizadorComplejidad(arbol)
    resultado = analizador.analizar('ejemplo')
    
    print(f"\nAnálisis original:")
    resultado.mostrar()
    
    # Guardar
    serializador = SerializadorAnalisis()
    ruta = serializador.guardar_analisis(codigo, resultado, "test_serialization")
    print(f"\nGuardado en: {ruta}")
    
    # Cargar
    datos_cargados = serializador.cargar_analisis(ruta)
    resultado_cargado = datos_cargados["resultado"]
    
    print(f"\nAnálisis cargado:")
    resultado_cargado.mostrar()
    
    # Verificar que son equivalentes
    original_str = str(resultado.funcion_tiempo.expr)
    cargado_str = str(resultado_cargado.funcion_tiempo.expr)
    
    print(f"\nComparación:")
    print(f"Original: {original_str}")
    print(f"Cargado:  {cargado_str}")
    print(f"Big O original: {resultado.big_o}")
    print(f"Big O cargado:  {resultado_cargado.big_o}")
    
    if resultado.big_o == resultado_cargado.big_o:
        print("✅ La serialización funciona correctamente!")
    else:
        print("❌ Hay diferencias en la serialización")

def probar_fibonacci():
    print("\n" + "="*50)
    print("=== Probando Fibonacci (Expresión Compleja) ===")
    
    codigo = '''
Funcion fibonacci(N)
    Si N <= 1 Entonces
        retornar N
    Sino
        retornar fibonacci(N-1) + fibonacci(N-2)
    fSi
fFuncion
'''
    
    print(f"Código:\n{codigo}")
    
    # Análisis
    tokens = tokenizar(codigo)
    arbol = parsear(tokens)
    analizador = AnalizadorComplejidad(arbol)
    resultado = analizador.analizar('fibonacci')
    
    print(f"\nAnálisis original:")
    resultado.mostrar()
    
    # Guardar
    serializador = SerializadorAnalisis()
    ruta = serializador.guardar_analisis(codigo, resultado, "test_fibonacci")
    print(f"\nGuardado en: {ruta}")
    
    # Cargar
    try:
        datos_cargados = serializador.cargar_analisis(ruta)
        resultado_cargado = datos_cargados["resultado"]
        
        print(f"\nAnálisis cargado:")
        resultado_cargado.mostrar()
        print("✅ Fibonacci cargado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al cargar fibonacci: {e}")

if __name__ == "__main__":
    probar_serializacion()
    probar_fibonacci()
