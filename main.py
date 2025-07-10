#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Complejidad Temporal para Pseudocódigo
===================================================

Este es el punto de entrada principal del analizador de complejidad temporal.
Permite analizar pseudocódigo y visualizar su complejidad temporal.

Autor: Proyecto ADA
Fecha: 2025
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

def main():
    """Función principal del programa"""
    print("═" * 65)
    print("     ANALIZADOR DE COMPLEJIDAD TEMPORAL")
    print("     Análisis de Pseudocódigo con Visualización")
    print("═" * 65)
    print()
    
    try:
        # Importar y ejecutar la interfaz gráfica
        from gui.app import AnalizadorApp
        
        print(" Iniciando interfaz gráfica...")
        print(" Tip: Usa 'python main.py --help' para ver opciones de CLI")
        print()
        
        app = AnalizadorApp()
        app.ejecutar()
        
    except ImportError as e:
        print(f" Error al importar módulos: {e}")
        print("\n Solución:")
        print("   pip install -r requirements.txt")
        print("\n También puedes ejecutar:")
        print("   python validar_sistema.py")
        sys.exit(1)
        
    except Exception as e:
        print(f" Error inesperado: {e}")
        print("\n Para más información, ejecuta:")
        print("   python validar_sistema.py")
        sys.exit(1)

def main_cli():
    """Función para ejecutar análisis desde línea de comandos"""
    if len(sys.argv) < 3:
        print("Uso: python main.py --cli <archivo_pseudocodigo> [opciones]")
        print("O simplemente: python main.py (para GUI)")
        print("\nOpciones:")
        print("  --verbose    Mostrar información detallada del análisis")
        print("  --save       Guardar el análisis automáticamente")
        print("\nEjemplos:")
        print("  python main.py --cli ejemplos/ejemplo_busqueda_lineal.txt")
        print("  python main.py --cli ejemplos/ejemplo_fibonacci_recursivo.txt --verbose")
        return
    
    archivo = sys.argv[2]
    verbose = "--verbose" in sys.argv
    auto_save = "--save" in sys.argv
    
    try:
        from core.pseudogrammar import tokenizar
        from core.parser_estructural import parsear
        from core.analizador_complejidad import AnalizadorComplejidad
        from core.serializacion import SerializadorAnalisis
        
        print("🔍 " + f"Analizando archivo: {archivo}")
        
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        if verbose:
            print("\n Código:")
            print("─" * 50)
            print(codigo)
            print("─" * 50)
        
        # Análisis
        if verbose:
            print("\n  Procesando...")
            print("  • Tokenizando código...")
        
        tokens = tokenizar(codigo)
        
        if verbose:
            print("  • Construyendo árbol sintáctico...")
        
        arbol = parsear(tokens)
        analizador = AnalizadorComplejidad(arbol)
        
        if verbose:
            print("  • Analizando complejidad...")
        
        # Buscar funciones
        funciones = []
        def encontrar_funciones(nodo):
            if nodo.tipo == 'FUNCION':
                nombre = nodo.props.get('nombre')
                if nombre:
                    funciones.append(nombre)
            for hijo in nodo.hijos:
                encontrar_funciones(hijo)
        
        encontrar_funciones(arbol)
        
        if funciones:
            resultado = analizador.analizar(funciones[0])
        else:
            resultado = analizador.analizar()
        
        print("\n📊 Resultado del análisis:")
        print("═" * 50)
        print(f" Función: {resultado.nombre_funcion or 'Código principal'}")
        print(f"  T(n) = {resultado.funcion_tiempo.como_str()}")
        print(f" Big O: {resultado.big_o}")
        print(f" Recursivo: {'Sí' if resultado.recursivo else 'No'}")
        
        if verbose:
            print(f"\n Detalles adicionales:")
            print(f"  • Tokens encontrados: {len(tokens)}")
            print(f"  • Funciones detectadas: {len(funciones)}")
            if funciones:
                print(f"  • Nombres de funciones: {', '.join(funciones)}")
        
        # Guardar automáticamente si se solicita
        if auto_save:
            try:
                serializador = SerializadorAnalisis()
                archivo_guardado = serializador.guardar_analisis(codigo, resultado)
                print(f"\n Análisis guardado en: {archivo_guardado}")
            except Exception as e:
                print(f"\n  Error al guardar: {e}")
        
        print("\n✅ Análisis completado exitosamente")
        
    except FileNotFoundError:
        print(f" Error: No se encontró el archivo '{archivo}'")
        print("💡 Verifica que la ruta sea correcta y el archivo exista")
    except Exception as e:
        print(f" Error durante el análisis: {e}")
        if verbose:
            import traceback
            print("\n🔍 Detalles del error:")
            traceback.print_exc()

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cli":
            main_cli()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(" ANALIZADOR DE COMPLEJIDAD TEMPORAL")
            print("═" * 50)
            print("\nUso:")
            print("  python main.py                    # Interfaz gráfica")
            print("  python main.py --cli <archivo>    # Análisis CLI")
            print("  python main.py --help             # Esta ayuda")
            print("  python main.py --ejemplos         # Listar ejemplos")
            print("\nOpciones CLI:")
            print("  --verbose    Mostrar información detallada")
            print("  --save       Guardar análisis automáticamente")
            print("\nEjemplos:")
            print("  python main.py --cli ejemplos/ejemplo_busqueda_lineal.txt")
            print("  python main.py --cli ejemplos/ejemplo_fibonacci_recursivo.txt --verbose")
            print("\nScripts adicionales:")
            print("  python probar_ejemplos.py         # Probar todos los ejemplos")
            print("  python validar_sistema.py         # Validar instalación")
        elif sys.argv[1] == "--ejemplos":
            print(" EJEMPLOS DISPONIBLES")
            print("═" * 50)
            ejemplos_dir = PROJECT_ROOT / "ejemplos"
            if ejemplos_dir.exists():
                ejemplos = list(ejemplos_dir.glob("*.txt"))
                if ejemplos:
                    ejemplos.sort()
                    print(f"\n{len(ejemplos)} ejemplos encontrados:\n")
                    for archivo in ejemplos:
                        nombre = archivo.stem.replace("ejemplo_", "").replace("_", " ").title()
                        print(f"  • {archivo.name:<35} | {nombre}")
                    print(f"\n💡 Para analizar un ejemplo:")
                    print(f"   python main.py --cli ejemplos/ejemplo_busqueda_lineal.txt")
                else:
                    print("No se encontraron ejemplos en la carpeta 'ejemplos/'")
            else:
                print("La carpeta 'ejemplos/' no existe")
        else:
            print(f"Argumento desconocido: {sys.argv[1]}")
            print("Usa 'python main.py --help' para ver las opciones disponibles")
    else:
        main()
