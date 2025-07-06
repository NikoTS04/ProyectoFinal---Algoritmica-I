# 🧪 Guía de Algoritmos para Pruebas

## Algoritmos por Complejidad Temporal

### O(1) - Constante
- `ejemplo_algoritmo_constante.txt` - Operaciones básicas

### O(log n) - Logarítmica
- `ejemplo_busqueda_binaria.txt` - Búsqueda binaria clásica
- `ejemplo_busqueda_ternaria.txt` - Búsqueda ternaria
- `ejemplo_recursion_logaritmica.txt` - Recursión logarítmica
- `ejemplo_mcd_euclidiano.txt` - Algoritmo de Euclides para MCD

### O(√n) - Raíz cuadrada
- `ejemplo_busqueda_jump.txt` - Jump search

### O(n) - Lineal
- `ejemplo_busqueda_lineal.txt` - Búsqueda lineal
- `ejemplo_suma_arreglo.txt` - Suma de elementos
- `ejemplo_buscar_maximo.txt` - Encontrar máximo
- `ejemplo_counting_sort.txt` - Counting sort (para rangos pequeños)

### O(n log n) - Lineal logarítmica
- `ejemplo_mergesort.txt` - Merge sort
- `ejemplo_heapsort.txt` - Heap sort
- `ejemplo_quicksort.txt` - Quick sort (caso promedio)
- `ejemplo_radix_sort.txt` - Radix sort

### O(n²) - Cuadrática
- `ejemplo_ordenamiento_burbuja.txt` - Bubble sort
- `ejemplo_ordenamiento_seleccion.txt` - Selection sort
- `ejemplo_insertion_sort.txt` - Insertion sort

### O(n³) - Cúbica
- `ejemplo_multiplicacion_matrices.txt` - Multiplicación de matrices

### O(2ⁿ) - Exponencial
- `ejemplo_fibonacci_recursivo.txt` - Fibonacci recursivo
- `ejemplo_torres_hanoi.txt` - Torres de Hanoi
- `ejemplo_generador_subconjuntos.txt` - Generador de subconjuntos

### O(n!) - Factorial
- `ejemplo_factorial_iterativo.txt` - Factorial iterativo
- `ejemplo_factorial_recursivo.txt` - Factorial recursivo

## Casos Especiales y Híbridos

### Algoritmos Adaptativos
- `ejemplo_busqueda_exponencial.txt` - Búsqueda exponencial
- `ejemplo_busqueda_interpolacion.txt` - Búsqueda por interpolación

### Programación Dinámica
- `ejemplo_mochila_dinamica.txt` - Problema de la mochila (O(nW))

### Divide y Vencerás
- `ejemplo_divide_conquista.txt` - Plantilla divide y vencerás
- `ejemplo_potencia_rapida.txt` - Exponenciación rápida

## 🎯 Recomendaciones para Pruebas

### Para Principiantes
1. Comienza con `ejemplo_algoritmo_constante.txt`
2. Prueba `ejemplo_suma_arreglo.txt` para O(n)
3. Experimenta con `ejemplo_ordenamiento_burbuja.txt` para O(n²)

### Para Comparaciones Interesantes
1. **Ordenamiento**: Compara burbuja vs merge vs quick sort
2. **Búsqueda**: Compara lineal vs binaria vs ternaria
3. **Factorial**: Compara iterativo vs recursivo
4. **Fibonacci**: Compara recursivo vs programación dinámica

### Para Casos Extremos
1. `ejemplo_torres_hanoi.txt` - Crecimiento exponencial
2. `ejemplo_fibonacci_recursivo.txt` - Recursión ineficiente
3. `ejemplo_generador_subconjuntos.txt` - Explosión combinatoria

## 🚀 Comandos de Prueba Rápida

```bash
# Interfaz gráfica
python main.py

# Análisis rápido desde CLI
python main.py --cli ejemplos/ejemplo_mergesort.txt

# Análisis detallado
python main.py --cli ejemplos/ejemplo_fibonacci_recursivo.txt --verbose

# Probar todos los ejemplos
python probar_ejemplos.py
```

## 📊 Resultados Esperados

| Algoritmo | Complejidad | Tipo | Recursivo |
|-----------|-------------|------|-----------|
| Constante | O(1) | Básico | No |
| Búsqueda Lineal | O(n) | Iterativo | No |
| Búsqueda Binaria | O(log n) | Divide y Vencerás | Sí |
| Merge Sort | O(n log n) | Divide y Vencerás | Sí |
| Bubble Sort | O(n²) | Comparación | No |
| Torres de Hanoi | O(2ⁿ) | Recursivo | Sí |
| Fibonacci Recursivo | O(2ⁿ) | Recursivo | Sí |

¡Disfruta probando los algoritmos! 🎉
