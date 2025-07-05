#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de utilidad para probar todos los ejemplos disponibles
y mostrar un resumen de sus complejidades.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

def probar_todos_ejemplos():
    """Analiza todos los ejemplos y muestra un resumen"""
    print("=" * 70)
    print("    ANALIZADOR DE EJEMPLOS - RESUMEN DE COMPLEJIDADES")
    print("=" * 70)
    print()
    
    try:
        from core.pseudogrammar import tokenizar
        from core.parser_estructural import parsear
        from core.analizador_complejidad import AnalizadorComplejidad
        
        ejemplos_dir = PROJECT_ROOT / "ejemplos"
        ejemplos = list(ejemplos_dir.glob("*.txt"))
        
        if not ejemplos:
            print("No se encontraron ejemplos en la carpeta 'ejemplos/'")
            return
        
        # Ordenar ejemplos por nombre
        ejemplos.sort()
        
        resultados = []
        
        print(f"Analizando {len(ejemplos)} ejemplos...\n")
        
        for archivo in ejemplos:
            nombre = archivo.stem.replace("ejemplo_", "").replace("_", " ").title()
            
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                
                # Análisis
                tokens = tokenizar(codigo)
                arbol = parsear(tokens)
                analizador = AnalizadorComplejidad(arbol)
                
                # Buscar funciones
                funciones = []
                def encontrar_funciones(nodo):
                    if nodo.tipo == 'FUNCION':
                        nombre_func = nodo.props.get('nombre')
                        if nombre_func:
                            funciones.append(nombre_func)
                    for hijo in nodo.hijos:
                        encontrar_funciones(hijo)
                
                encontrar_funciones(arbol)
                
                if funciones:
                    resultado = analizador.analizar(funciones[0])
                else:
                    resultado = analizador.analizar()
                
                resultados.append({
                    'nombre': nombre,
                    'archivo': archivo.name,
                    'funcion': resultado.nombre_funcion or "Sin nombre",
                    'big_o': resultado.big_o,
                    'expresion': resultado.funcion_tiempo.como_str(),
                    'recursivo': resultado.recursivo
                })
                
                print(f"✓ {nombre:<25} | {resultado.big_o:<10} | {resultado.funcion_tiempo.como_str()}")
                
            except Exception as e:
                print(f"✗ {nombre:<25} | ERROR     | {str(e)[:30]}...")
                continue
        
        # Mostrar resumen por complejidad
        print("\n" + "=" * 70)
        print("RESUMEN POR COMPLEJIDAD")
        print("=" * 70)
        
        complejidades = {}
        for r in resultados:
            big_o = r['big_o']
            if big_o not in complejidades:
                complejidades[big_o] = []
            complejidades[big_o].append(r)
        
        # Ordenar por complejidad (aproximado)
        orden_complejidad = ['O(1)', 'O(log(n))', 'O(n)', 'O(n**2)', 'O(n**3)', 'O(2^n)']
        
        for big_o in orden_complejidad:
            if big_o in complejidades:
                print(f"\n{big_o}:")
                for algo in complejidades[big_o]:
                    print(f"  • {algo['nombre']} ({algo['archivo']})")
        
        # Mostrar otras complejidades no clasificadas
        for big_o, algoritmos in complejidades.items():
            if big_o not in orden_complejidad:
                print(f"\n{big_o}:")
                for algo in algoritmos:
                    print(f"  • {algo['nombre']} ({algo['archivo']})")
        
        print(f"\n{'-' * 70}")
        print(f"Total de ejemplos analizados: {len(resultados)}")
        print(f"Tipos de complejidad encontrados: {len(complejidades)}")
        
        # Sugerencias de uso
        print(f"\n{'SUGERENCIAS DE USO':^70}")
        print(f"{'-' * 70}")
        print("• Para analizar un ejemplo específico:")
        print("  python main.py --cli ejemplos/ejemplo_ordenamiento_burbuja.txt")
        print("\n• Para usar la interfaz gráfica:")
        print("  python main.py")
        print("\n• Para comparar algoritmos, usa la pestaña 'Comparación' en la GUI")
        
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    probar_todos_ejemplos()
