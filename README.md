# Analizador de Complejidad Temporal

Este proyecto es un analizador de complejidad temporal para pseudocódigo que sigue una gramática específica. Utiliza expresiones regulares para tokenización, parsing estructural para crear un árbol de sintaxis abstracta, y análisis simbólico para determinar la complejidad temporal.

## 🚀 Inicio Rápido

### Ejecutar la Aplicación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar interfaz gráfica
python main.py

# Ver ayuda completa
python main.py --help

# Listar ejemplos disponibles
python main.py --ejemplos

# Análisis desde línea de comandos
python main.py --cli ejemplos/ejemplo_busqueda_lineal.txt

# Análisis detallado con guardado automático
python main.py --cli ejemplos/ejemplo_fibonacci_recursivo.txt --verbose --save
```

## 📁 Estructura del Proyecto

```
├── main.py                    # Punto de entrada principal
├── controller.py              # Ejemplo de uso básico
├── requirements.txt           # Dependencias
├── README.md                 # Este archivo
├── GUIA_USUARIO.md           # Guía de inicio rápido
├── CONSEJOS_Y_TRUCOS.md      # Tips y atajos útiles
├── ESTADO_PROYECTO.md        # Estado del desarrollo
├── probar_ejemplos.py        # Script para probar todos los ejemplos
├── validar_sistema.py        # Script de validación completa
├── src/                      # Código fuente
│   ├── core/                 # Lógica principal
│   │   ├── pseudogrammar.py          # Tokenización
│   │   ├── parser_estructural.py     # Parsing y AST
│   │   ├── analizador_expresiones.py # Conteo de operaciones
│   │   ├── expresion_simbolica.py    # Matemática simbólica
│   │   ├── analizador_complejidad.py # Análisis principal
│   │   └── serializacion.py          # Guardar/cargar
│   └── gui/                  # Interfaz gráfica
│       ├── app.py            # Aplicación principal
│       ├── entrada.py        # Pestaña de entrada
│       ├── grafica.py        # Pestaña de gráficas
│       └── comparacion.py    # Pestaña de comparación
├── ejemplos/                 # Archivos de ejemplo
│   ├── ejemplo_busqueda_lineal.txt
│   ├── ejemplo_busqueda_binaria.txt
│   ├── ejemplo_fibonacci_recursivo.txt
│   ├── ejemplo_ordenamiento_burbuja.txt
│   ├── ejemplo_multiplicacion_matrices.txt
│   ├── ... (12 ejemplos más)
│   └── README.md             # Documentación de ejemplos
└── analisis_guardados/       # Análisis guardados
```

## ✨ Funcionalidades

### 🔍 Análisis de Complejidad Temporal
- Tokenización con expresiones regulares
- Parsing estructural para crear AST
- Análisis de operaciones básicas
- Soporte para bucles (Para, Mientras)
- Análisis de estructuras condicionales (Si/Sino)
- Detección de funciones recursivas
- Cálculo de Big O notation

### 🖥️ Interfaz Gráfica Moderna
- **Pestaña Entrada**: Editor de código con análisis automático
- **Pestaña Gráfica**: Visualización integrada con matplotlib
- **Pestaña Comparación**: Comparación visual entre algoritmos

### 💾 Persistencia
- Guardar análisis en archivos JSON
- Cargar análisis previamente guardados
- Sistema de metadatos y versionado

### 📊 Visualización Avanzada
- Gráficas T(n) integradas en la interfaz
- Comparación T(n) vs Big O
- Barra de herramientas de navegación
- Exportación de gráficas como imagen

## Sintaxis del Pseudocódigo

### Estructura Básica
```
Funcion nombreFuncion(parametros)
    // contenido
fFuncion
```

### Ejemplos Soportados

#### Bucle Para
```
Para i desde 1 hasta N hacer
    x <- x + 1
fPara
```

#### Bucle Mientras
```
Mientras i <= N hacer
    x <- x + 1
    i <- i + 1
fMientras
```

#### Condicionales
```
Si x > 0 Entonces
    y <- x * 2
Sino
    y <- 0
fSi
```

#### Recursión
```
Funcion fibonacci(N)
    Si N <= 1 Entonces
        retornar N
    Sino
        retornar fibonacci(N-1) + fibonacci(N-2)
    fSi
fFuncion
```

## Archivos de Ejemplo

El proyecto incluye una amplia colección de ejemplos que cubren diferentes tipos de complejidades:

### Complejidad Constante O(1)
- `ejemplo_algoritmo_constante.txt`: Operaciones independientes del tamaño de entrada

### Complejidad Lineal O(n)
- `ejemplo_busqueda_lineal.txt`: Búsqueda secuencial básica
- `ejemplo_busqueda_secuencial.txt`: Búsqueda con bucle Mientras
- `ejemplo_suma_arreglo.txt`: Suma de elementos de un arreglo
- `ejemplo_buscar_maximo.txt`: Encontrar el elemento máximo
- `ejemplo_factorial_iterativo.txt`: Factorial con bucle Para

### Complejidad Logarítmica O(log n)
- `ejemplo_busqueda_binaria.txt`: Búsqueda binaria clásica
- `ejemplo_divide_conquista.txt`: Patrón divide y vencerás
- `ejemplo_potencia_rapida.txt`: Exponenciación rápida

### Complejidad Cuadrática O(n²)
- `ejemplo_ordenamiento_burbuja.txt`: Algoritmo burbuja con bucles anidados
- `ejemplo_ordenamiento_seleccion.txt`: Ordenamiento por selección

### Complejidad Cúbica O(n³)
- `ejemplo_multiplicacion_matrices.txt`: Multiplicación de matrices con tres bucles anidados

### Complejidad Exponencial O(2ⁿ)
- `ejemplo_fibonacci_recursivo.txt`: Fibonacci con doble recursión
- `ejemplo_factorial_recursivo.txt`: Factorial recursivo lineal
- `ejemplo_exponencial.txt`: Algoritmo exponencial genérico

### 🔧 Script de Utilidad
Para probar todos los ejemplos automáticamente:
```bash
python probar_ejemplos.py
```

Este script analiza todos los ejemplos y genera un resumen de complejidades, perfecto para verificar el funcionamiento del analizador.

## 🛠️ Scripts de Utilidad

### `probar_ejemplos.py`
Script que analiza automáticamente todos los ejemplos y genera un resumen:
```bash
python probar_ejemplos.py
```
- Muestra la complejidad de cada ejemplo
- Agrupa algoritmos por tipo de complejidad
- Perfecto para verificar el funcionamiento del analizador

### `validar_sistema.py`
Script de validación completa del sistema:
```bash
python validar_sistema.py
```
- Verifica que todas las dependencias estén instaladas
- Valida que todos los módulos funcionen correctamente
- Prueba la serialización y carga de análisis
- Confirma que la interfaz gráfica esté operativa
```

## Arquitectura del Proyecto

```
├── pseudogrammar.py          # Tokenización con regex
├── parser_estructural.py     # Parsing y AST
├── analizador_expresiones.py # Conteo de operaciones
├── expresion_simbolica.py    # Matemática simbólica
├── analizador_complejidad.py # Análisis principal
├── serializacion.py          # Guardar/cargar análisis
├── controller.py             # Ejemplo de uso básico
├── test_interfaz.py          # Ejecutar GUI
└── front/                    # Interfaz gráfica
    ├── frame.py              # Ventana principal
    ├── entrada.py            # Pestaña de entrada
    ├── grafica.py            # Pestaña de gráficas
    └── comparacion.py        # Pestaña de comparación
```

## Dependencias

- `sympy`: Matemática simbólica
- `matplotlib`: Gráficas
- `ttkbootstrap`: Interfaz moderna
- `numpy`: Cálculos numéricos

## Limitaciones Conocidas

1. La gramática está limitada a las construcciones implementadas
2. El análisis de recursión es básico
3. No maneja estructuras de datos complejas
4. El análisis de peor caso puede ser aproximado

## Desarrollo Futuro

- Mejor análisis de recursión
- Soporte para más estructuras de control
- Análisis de espacio además de tiempo
- Mejor detección de patrones de complejidad
- Exportación de reportes completos
