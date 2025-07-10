#!/usr/bin/env python3
"""
Script para validar automáticamente todos los ejemplos de algoritmos
y verificar que el analizador de complejidad detecte correctamente T(n) y Big O.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def obtener_archivos_ejemplo():
    """Obtiene todos los archivos .txt de la carpeta ejemplos/"""
    carpeta_ejemplos = Path("ejemplos")
    if not carpeta_ejemplos.exists():
        print("❌ No se encontró la carpeta 'ejemplos/'")
        return []
    
    archivos = list(carpeta_ejemplos.glob("*.txt"))
    return sorted(archivos)

def ejecutar_analizador(archivo_ejemplo):
    """Ejecuta el analizador para un archivo específico"""
    try:
        # Usar Python del entorno virtual
        python_exe = r"C:/Users/tarqu/OneDrive/Documentos/ADAProyecto/ProyectoFinal---Algoritmica-I/.venv/Scripts/python.exe"
        
        # Ejecutar el comando principal con --cli
        cmd = [python_exe, "main.py", "--cli", str(archivo_ejemplo)]
        
        # Configurar el entorno para UTF-8 en Windows
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, 
                              encoding='utf-8', errors='replace', env=env)
        
        if result.returncode != 0:
            return {
                'archivo': archivo_ejemplo.name,
                'error': f"Error de ejecución: {result.stderr}",
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        
        # Parsear la salida para extraer T(n) y Big O
        salida = result.stdout
        return parsear_salida_analizador(archivo_ejemplo.name, salida)
        
    except subprocess.TimeoutExpired:
        return {
            'archivo': archivo_ejemplo.name,
            'error': "Timeout - el análisis tardó más de 30 segundos"
        }
    except Exception as e:
        return {
            'archivo': archivo_ejemplo.name,
            'error': f"Excepción: {str(e)}"
        }

def parsear_salida_analizador(nombre_archivo, salida):
    """Extrae T(n) y Big O de la salida del analizador"""
    resultado = {
        'archivo': nombre_archivo,
        'tn': None,
        'big_o': None,
        'recursivo': False,
        'funcion': None,
        'salida_completa': salida
    }
    
    lineas = salida.split('\n')
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        
        # Buscar función analizada
        if linea.startswith("Función: '") and "': " in linea:
            inicio = linea.find("'") + 1
            fin = linea.find("'", inicio)
            if fin > inicio:
                resultado['funcion'] = linea[inicio:fin]
        
        # Buscar si es recursiva
        if "(recursiva)" in linea:
            resultado['recursivo'] = True
        
        # Buscar T(n)
        if "T(n) =" in linea:
            tn_parte = linea.split("T(n) =", 1)[1].strip()
            resultado['tn'] = tn_parte
        
        # Buscar Big O
        if "Big O:" in linea:
            big_o_parte = linea.split("Big O:", 1)[1].strip()
            resultado['big_o'] = big_o_parte
    
    return resultado

def clasificar_algoritmo_esperado(nombre_archivo):
    """Clasifica la complejidad esperada basada en el nombre del archivo"""
    nombre = nombre_archivo.lower()
    
    # Algoritmos constantes O(1)
    if 'constante' in nombre:
        return 'O(1)', 'Constante'
    
    # Algoritmos logarítmicos O(log n)
    elif any(palabra in nombre for palabra in ['binaria', 'ternaria', 'potencia_rapida', 'logaritmica']):
        return 'O(log(N))', 'Logarítmico'
    
    # Algoritmos lineales O(n)
    elif any(palabra in nombre for palabra in ['lineal', 'suma_arreglo', 'buscar_maximo', 'counting_sort', 'radix_sort']):
        return 'O(N)', 'Lineal'
    
    # Algoritmos O(n log n)
    elif any(palabra in nombre for palabra in ['mergesort', 'quicksort', 'heapsort']):
        return 'O(N*log(N))', 'n log n'
    
    # Algoritmos cuadráticos O(n²)
    elif any(palabra in nombre for palabra in ['burbuja', 'seleccion', 'insertion']):
        return 'O(N**2)', 'Cuadrático'
    
    # Algoritmos cúbicos O(n³)
    elif 'multiplicacion_matrices' in nombre:
        return 'O(N**3)', 'Cúbico'
    
    # Algoritmos exponenciales O(2^n)
    elif any(palabra in nombre for palabra in ['fibonacci_recursivo', 'hanoi']):
        return 'O(2**N)', 'Exponencial'
    
    # Algoritmos con múltiples variables O(n*m)
    elif 'mochila' in nombre:
        return 'O(N*W)', 'O(n*m)'
    
    # Factorial iterativo/recursivo O(n)
    elif 'factorial' in nombre:
        return 'O(N)', 'Lineal (factorial)'
    
    # Divide y vencerás
    elif 'divide_conquista' in nombre:
        return 'O(N*log(N))', 'Divide y vencerás'
    
    # Recursión condicional
    elif 'recursion_condicional' in nombre:
        return 'O(log(N))', 'Recursión condicional'
    
    else:
        return 'Desconocido', 'No clasificado'

def normalizar_big_o(big_o_str):
    """Normaliza diferentes representaciones de Big O para comparación"""
    if not big_o_str:
        return ""
    
    # Limpiar espacios y convertir a minúsculas
    normalizado = big_o_str.strip().lower()
    
    # Mapear variaciones comunes
    mapeos = {
        'o(1)': 'O(1)',
        'o(n)': 'O(N)',
        'o(log n)': 'O(log(N))',
        'o(log(n))': 'O(log(N))',
        'o(n log n)': 'O(N*log(N))',
        'o(n*log(n))': 'O(N*log(N))',
        'o(n^2)': 'O(N**2)',
        'o(n**2)': 'O(N**2)',
        'o(n²)': 'O(N**2)',
        'o(n^3)': 'O(N**3)',
        'o(n**3)': 'O(N**3)',
        'o(n³)': 'O(N**3)',
        'o(2^n)': 'O(2**N)',
        'o(2**n)': 'O(2**N)',
        'o(n*m)': 'O(N*M)',
        'o(n*w)': 'O(N*W)',
    }
    
    for patron, resultado in mapeos.items():
        if patron in normalizado:
            return resultado
    
    return big_o_str

def es_big_o_correcto(esperado, obtenido):
    """Verifica si el Big O obtenido coincide con el esperado"""
    if not esperado or not obtenido:
        return False
    
    esperado_norm = normalizar_big_o(esperado)
    obtenido_norm = normalizar_big_o(obtenido)
    
    return esperado_norm == obtenido_norm

def generar_reporte(resultados):
    """Genera un reporte detallado de los resultados"""
    print("\n" + "="*80)
    print("REPORTE DE VALIDACIÓN DE EJEMPLOS")
    print("="*80)
    
    correctos = 0
    incorrectos = 0
    errores = 0
    
    # Agrupar por categoría
    categorias = {}
    
    for resultado in resultados:
        if 'error' in resultado:
            errores += 1
            continue
        
        nombre = resultado['archivo']
        big_o_esperado, categoria = clasificar_algoritmo_esperado(nombre)
        
        if categoria not in categorias:
            categorias[categoria] = []
        
        es_correcto = es_big_o_correcto(big_o_esperado, resultado['big_o'])
        if es_correcto:
            correctos += 1
        else:
            incorrectos += 1
        
        categorias[categoria].append({
            'archivo': nombre,
            'esperado': big_o_esperado,
            'obtenido': resultado['big_o'],
            'tn': resultado['tn'],
            'correcto': es_correcto,
            'recursivo': resultado['recursivo'],
            'funcion': resultado.get('funcion', 'N/A')
        })
    
    # Mostrar resumen por categoría
    for categoria, items in sorted(categorias.items()):
        print(f"\n📂 {categoria.upper()}")
        print("-" * 60)
        
        for item in items:
            estado = "✅" if item['correcto'] else "❌"
            recursivo_str = " (recursiva)" if item['recursivo'] else ""
            
            print(f"{estado} {item['archivo']}")
            print(f"   Función: {item['funcion']}{recursivo_str}")
            print(f"   Esperado: {item['esperado']}")
            print(f"   Obtenido: {item['obtenido']}")
            print(f"   T(n): {item['tn']}")
            print()
    
    # Mostrar errores
    if errores > 0:
        print("\n🚨 ERRORES ENCONTRADOS")
        print("-" * 40)
        for resultado in resultados:
            if 'error' in resultado:
                print(f"❌ {resultado['archivo']}: {resultado['error']}")
                if resultado.get('stdout'):
                    print(f"   Salida: {resultado['stdout'][:200]}...")
                print()
    
    # Resumen final
    total = len(resultados)
    print("\n📊 RESUMEN FINAL")
    print("-" * 40)
    print(f"Total de ejemplos: {total}")
    print(f"✅ Correctos: {correctos}")
    print(f"❌ Incorrectos: {incorrectos}")
    print(f"🚨 Errores: {errores}")
    
    if total > 0:
        porcentaje_exito = (correctos / (total - errores)) * 100 if (total - errores) > 0 else 0
        print(f"📈 Tasa de éxito: {porcentaje_exito:.1f}%")
    
    return correctos, incorrectos, errores

def guardar_resultados_json(resultados, archivo_salida="resultados_validacion.json"):
    """Guarda los resultados en formato JSON para análisis posterior"""
    from datetime import datetime
    
    datos_salida = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_ejemplos': len(resultados),
        'resultados': []
    }
    
    for resultado in resultados:
        if 'error' not in resultado:
            nombre = resultado['archivo']
            big_o_esperado, categoria = clasificar_algoritmo_esperado(nombre)
            
            datos_salida['resultados'].append({
                'archivo': nombre,
                'categoria': categoria,
                'funcion': resultado.get('funcion'),
                'big_o_esperado': big_o_esperado,
                'big_o_obtenido': resultado['big_o'],
                'tn_obtenido': resultado['tn'],
                'es_correcto': es_big_o_correcto(big_o_esperado, resultado['big_o']),
                'es_recursivo': resultado['recursivo']
            })
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_salida, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados guardados en: {archivo_salida}")
    except Exception as e:
        print(f"\n⚠️  Error al guardar resultados: {e}")

def main():
    print("🔍 VALIDADOR AUTOMÁTICO DE EJEMPLOS")
    print("=" * 50)
    
    # Obtener archivos de ejemplo
    archivos = obtener_archivos_ejemplo()
    if not archivos:
        print("❌ No se encontraron archivos de ejemplo para procesar.")
        return
    
    print(f"📁 Encontrados {len(archivos)} archivos de ejemplo")
    print()
    
    # Procesar cada archivo
    resultados = []
    for i, archivo in enumerate(archivos, 1):
        print(f"[{i:2d}/{len(archivos)}] Procesando: {archivo.name}... ", end="", flush=True)
        
        resultado = ejecutar_analizador(archivo)
        resultados.append(resultado)
        
        if 'error' in resultado:
            print("❌ ERROR")
        elif resultado['big_o']:
            print(f"✅ {resultado['big_o']}")
        else:
            print("⚠️  Sin resultado")
    
    # Generar reporte
    correctos, incorrectos, errores = generar_reporte(resultados)
    
    # Guardar resultados
    guardar_resultados_json(resultados)
    
    # Código de salida
    if errores > 0:
        sys.exit(2)  # Errores críticos
    elif incorrectos > 0:
        sys.exit(1)  # Resultados incorrectos
    else:
        sys.exit(0)  # Todo correcto

if __name__ == "__main__":
    main()
