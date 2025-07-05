# Ejemplos para el Analizador de Complejidad Temporal

Este directorio contiene una colección de ejemplos de pseudocódigo que demuestran diferentes tipos de complejidades temporales. Cada archivo puede ser analizado con el analizador para observar su comportamiento y complejidad.

## 📁 Lista de Ejemplos

### Complejidad Constante - O(1)
- **`ejemplo_algoritmo_constante.txt`**
  - **Descripción**: Algoritmo que realiza operaciones independientes del tamaño de entrada
  - **Complejidad**: O(1)
  - **Características**: Asignaciones simples, operaciones aritméticas básicas

### Complejidad Lineal - O(n)
- **`ejemplo_busqueda_lineal.txt`**
  - **Descripción**: Búsqueda secuencial en un arreglo
  - **Complejidad**: O(n)
  - **Características**: Un solo bucle que recorre todos los elementos

- **`ejemplo_busqueda_secuencial.txt`**
  - **Descripción**: Búsqueda con bucle Mientras y condiciones
  - **Complejidad**: O(n)
  - **Características**: Bucle Mientras con condición de parada

- **`ejemplo_suma_arreglo.txt`**
  - **Descripción**: Suma todos los elementos de un arreglo
  - **Complejidad**: O(n)
  - **Características**: Recorrido simple con acumulación

- **`ejemplo_buscar_maximo.txt`**
  - **Descripción**: Encuentra el elemento máximo en un arreglo
  - **Complejidad**: O(n)
  - **Características**: Recorrido con comparaciones condicionales

- **`ejemplo_factorial_iterativo.txt`**
  - **Descripción**: Cálculo iterativo del factorial
  - **Complejidad**: O(n)
  - **Características**: Bucle con multiplicación acumulativa

### Complejidad Logarítmica - O(log n)
- **`ejemplo_busqueda_binaria.txt`**
  - **Descripción**: Búsqueda binaria en arreglo ordenado
  - **Complejidad**: O(log n)
  - **Características**: División del espacio de búsqueda en cada iteración

- **`ejemplo_divide_conquista.txt`**
  - **Descripción**: Algoritmo genérico de divide y vencerás
  - **Complejidad**: O(log n)
  - **Características**: Reducción del problema a la mitad en cada paso

- **`ejemplo_potencia_rapida.txt`**
  - **Descripción**: Exponenciación rápida por cuadratura
  - **Complejidad**: O(log n)
  - **Características**: Recursión con división por 2

### Complejidad Cuadrática - O(n²)
- **`ejemplo_ordenamiento_burbuja.txt`**
  - **Descripción**: Algoritmo de ordenamiento burbuja
  - **Complejidad**: O(n²)
  - **Características**: Dos bucles anidados

- **`ejemplo_ordenamiento_seleccion.txt`**
  - **Descripción**: Algoritmo de ordenamiento por selección
  - **Complejidad**: O(n²)
  - **Características**: Bucles anidados con búsqueda del mínimo

### Complejidad Cúbica - O(n³)
- **`ejemplo_multiplicacion_matrices.txt`**
  - **Descripción**: Multiplicación de matrices cuadradas
  - **Complejidad**: O(n³)
  - **Características**: Tres bucles anidados

### Complejidad Exponencial - O(2ⁿ)
- **`ejemplo_fibonacci_recursivo.txt`**
  - **Descripción**: Cálculo recursivo de Fibonacci
  - **Complejidad**: O(2ⁿ)
  - **Características**: Doble recursión

- **`ejemplo_factorial_recursivo.txt`**
  - **Descripción**: Cálculo recursivo del factorial
  - **Complejidad**: O(n) - Recursión lineal
  - **Características**: Recursión simple con un solo llamado

- **`ejemplo_exponencial.txt`**
  - **Descripción**: Algoritmo exponencial genérico
  - **Complejidad**: O(2ⁿ)
  - **Características**: Múltiples llamadas recursivas

## 🎯 Cómo usar los ejemplos

### Desde la Interfaz Gráfica
1. Ejecuta `python main.py`
2. En la pestaña "Entrada", haz clic en "Cargar archivo"
3. Selecciona cualquier archivo de la carpeta `ejemplos/`
4. El análisis se realizará automáticamente
5. Ve a la pestaña "Gráfica" para visualizar los resultados

### Desde Línea de Comandos
```bash
python main.py --cli ejemplos/ejemplo_ordenamiento_burbuja.txt
```

### Para Comparaciones
1. Analiza un algoritmo en la pestaña "Entrada"
2. Ve a la pestaña "Comparación"
3. Carga otro ejemplo usando "Cargar desde archivo"
4. Haz clic en "Comparar" para ver la comparación visual

## 📊 Resultados Esperados

| Ejemplo | Complejidad | Big O | Características |
|---------|-------------|-------|-----------------|
| Algoritmo Constante | O(1) | O(1) | Tiempo fijo |
| Búsqueda Lineal | O(n) | O(n) | Crecimiento lineal |
| Búsqueda Binaria | O(log n) | O(log n) | Crecimiento logarítmico |
| Ordenamiento Burbuja | O(n²) | O(n²) | Crecimiento cuadrático |
| Multiplicación Matrices | O(n³) | O(n³) | Crecimiento cúbico |
| Fibonacci Recursivo | O(2ⁿ) | O(2ⁿ) | Crecimiento exponencial |

## 💡 Consejos de Uso

1. **Experimenta con diferentes tamaños**: Los algoritmos exponenciales se vuelven muy costosos rápidamente
2. **Compara algoritmos similares**: Por ejemplo, factorial recursivo vs iterativo
3. **Observa las gráficas**: Las diferencias entre complejidades se hacen evidentes visualmente
4. **Prueba modificaciones**: Cambia los ejemplos para ver cómo afecta la complejidad

## 🔧 Creando tus propios ejemplos

Para crear nuevos ejemplos, sigue la sintaxis del pseudocódigo:

```
Funcion nombreFuncion(N)
    // Tu algoritmo aquí
    // Usa Para, Mientras, Si/Sino
    // Termina con retornar
fFuncion
```

¡Guarda el archivo con extensión `.txt` y analízalo con la herramienta!
