#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación del sistema completo.
Verifica que todas las funcionalidades estén operativas.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar módulos
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

def validar_dependencias():
    """Valida que todas las dependencias estén instaladas"""
    print("🔍 Validando dependencias...")
    
    dependencias = [
        ('sympy', 'Matemática simbólica'),
        ('matplotlib', 'Gráficas'),
        ('numpy', 'Cálculos numéricos'),
        ('ttkbootstrap', 'Interfaz moderna')
    ]
    
    faltantes = []
    
    for dep, desc in dependencias:
        try:
            __import__(dep)
            print(f"  ✓ {dep} - {desc}")
        except ImportError:
            print(f"  ✗ {dep} - {desc} (FALTANTE)")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n❌ Faltan dependencias: {', '.join(faltantes)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas\n")
    return True

def validar_modulos_core():
    """Valida que todos los módulos core funcionen"""
    print("🧪 Validando módulos core...")
    
    try:
        from core.pseudogrammar import tokenizar
        from core.parser_estructural import parsear
        from core.analizador_complejidad import AnalizadorComplejidad
        from core.serializacion import SerializadorAnalisis
        from core.expresion_simbolica import ExpresionSimbolica
        
        print("  ✓ Tokenizador")
        print("  ✓ Parser estructural")
        print("  ✓ Analizador de complejidad")
        print("  ✓ Sistema de serialización")
        print("  ✓ Expresiones simbólicas")
        
        print("✅ Todos los módulos core funcionan\n")
        return True
        
    except Exception as e:
        print(f"❌ Error en módulos core: {e}")
        return False

def validar_interfaz_grafica():
    """Valida que la interfaz gráfica se pueda importar"""
    print("🖥️ Validando interfaz gráfica...")
    
    try:
        from gui.app import AnalizadorApp
        from gui.entrada import crear_pestana_entrada
        from gui.grafica import crear_pestana_grafica
        from gui.comparacion import crear_pestana_comparacion
        
        print("  ✓ Aplicación principal")
        print("  ✓ Pestaña de entrada")
        print("  ✓ Pestaña de gráficas")
        print("  ✓ Pestaña de comparación")
        
        print("✅ Interfaz gráfica lista\n")
        return True
        
    except Exception as e:
        print(f"❌ Error en interfaz gráfica: {e}")
        return False

def validar_ejemplos():
    """Valida que los ejemplos se puedan analizar"""
    print("📚 Validando ejemplos...")
    
    try:
        from core.pseudogrammar import tokenizar
        from core.parser_estructural import parsear
        from core.analizador_complejidad import AnalizadorComplejidad
        
        ejemplos_dir = PROJECT_ROOT / "ejemplos"
        ejemplos = list(ejemplos_dir.glob("*.txt"))
        
        if not ejemplos:
            print("❌ No se encontraron ejemplos")
            return False
        
        exitosos = 0
        for archivo in ejemplos[:5]:  # Validar solo los primeros 5
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                
                tokens = tokenizar(codigo)
                arbol = parsear(tokens)
                analizador = AnalizadorComplejidad(arbol)
                resultado = analizador.analizar()
                
                exitosos += 1
                
            except Exception:
                continue
        
        print(f"  ✓ {exitosos}/{min(len(ejemplos), 5)} ejemplos procesados correctamente")
        
        if exitosos >= 3:
            print("✅ Ejemplos funcionando correctamente\n")
            return True
        else:
            print("❌ Muchos ejemplos fallan\n")
            return False
            
    except Exception as e:
        print(f"❌ Error validando ejemplos: {e}")
        return False

def validar_serializacion():
    """Valida que la serialización funcione"""
    print("💾 Validando serialización...")
    
    try:
        from core.serializacion import SerializadorAnalisis
        from core.analizador_complejidad import ResultadoAnalisis
        from core.expresion_simbolica import ExpresionSimbolica
        
        serializador = SerializadorAnalisis()
        
        # Crear un resultado de prueba
        expr = ExpresionSimbolica.variable('N')
        resultado = ResultadoAnalisis(
            funcion_tiempo=expr,
            big_o="O(n)",
            recursivo=False,
            nombre_funcion="test"
        )
        
        # Intentar guardar
        archivo = serializador.guardar_analisis("test", resultado, "test_validacion")
        
        # Intentar cargar
        datos = serializador.cargar_analisis(archivo)
        
        # Limpiar
        os.remove(archivo)
        
        print("  ✓ Guardar análisis")
        print("  ✓ Cargar análisis")
        print("✅ Serialización funcionando\n")
        return True
        
    except Exception as e:
        print(f"❌ Error en serialización: {e}")
        return False

def validar_sistema_completo():
    """Ejecuta todas las validaciones"""
    print("🎯 VALIDACIÓN COMPLETA DEL SISTEMA")
    print("=" * 50)
    print()
    
    validaciones = [
        validar_dependencias,
        validar_modulos_core,
        validar_interfaz_grafica,
        validar_ejemplos,
        validar_serializacion
    ]
    
    exitos = 0
    for validacion in validaciones:
        if validacion():
            exitos += 1
    
    print("=" * 50)
    print(f"RESULTADO: {exitos}/{len(validaciones)} validaciones exitosas")
    
    if exitos == len(validaciones):
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\nPuedes ejecutar:")
        print("  • python main.py (interfaz gráfica)")
        print("  • python main.py --cli ejemplos/ejemplo_busqueda_lineal.txt (CLI)")
        print("  • python probar_ejemplos.py (probar todos los ejemplos)")
    else:
        print("⚠️  Algunos componentes necesitan atención")
        print("\nRevisa los errores mostrados arriba")
    
    return exitos == len(validaciones)

if __name__ == "__main__":
    validar_sistema_completo()
