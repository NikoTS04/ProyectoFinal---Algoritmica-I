# Guía de Inicio Rápido - Analizador de Complejidad Temporal

¡Bienvenido al Analizador de Complejidad Temporal! Esta guía te ayudará a comenzar rápidamente.

## 🚀 Instalación y Configuración

### 1. Verificar Python
Asegúrate de tener Python 3.8 o superior:
```bash
python --version
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar Instalación
```bash
python probar_ejemplos.py
```

## 🎯 Primeros Pasos

### Opción 1: Interfaz Gráfica (Recomendado)
```bash
python main.py
```

**Flujo de trabajo sugerido:**
1. **Pestaña Entrada**: Carga un ejemplo desde `ejemplos/ejemplo_busqueda_lineal.txt`
2. **Pestaña Gráfica**: Observa la visualización de T(n) vs Big O
3. **Pestaña Comparación**: Carga otro algoritmo y compara

### Opción 2: Línea de Comandos
```bash
python main.py --cli ejemplos/ejemplo_ordenamiento_burbuja.txt
```

## 📁 Ejemplos Recomendados para Empezar

### Para Principiantes:
1. `ejemplo_algoritmo_constante.txt` - Muy simple, O(1)
2. `ejemplo_suma_arreglo.txt` - Lineal básico, O(n)
3. `ejemplo_ordenamiento_burbuja.txt` - Cuadrático, O(n²)

### Para Comparaciones Interesantes:
- **Factorial**: Compara `ejemplo_factorial_iterativo.txt` vs `ejemplo_factorial_recursivo.txt`
- **Búsquedas**: Compara `ejemplo_busqueda_lineal.txt` vs `ejemplo_busqueda_binaria.txt`
- **Ordenamientos**: Compara `ejemplo_ordenamiento_burbuja.txt` vs `ejemplo_ordenamiento_seleccion.txt`

### Para Casos Avanzados:
- `ejemplo_fibonacci_recursivo.txt` - Exponencial O(2ⁿ)
- `ejemplo_multiplicacion_matrices.txt` - Cúbico O(n³)

## 🛠️ Funcionalidades Principales

### 1. Análisis Automático
- El analizador detecta automáticamente bucles, condicionales y recursión
- Calcula la función T(n) y el Big O correspondiente
- Identifica si el algoritmo es recursivo

### 2. Visualización
- Gráficas integradas con matplotlib
- Comparación visual T(n) vs Big O teórico
- Herramientas de zoom y navegación

### 3. Comparación de Algoritmos
- Carga dos algoritmos diferentes
- Visualización comparativa en tiempo real
- Análisis automático de eficiencia

### 4. Persistencia
- Guarda análisis en formato JSON
- Carga análisis previos para comparación
- Metadatos y versionado automático

## 📝 Sintaxis del Pseudocódigo

### Estructura Básica
```
Funcion nombreFuncion(N)
    // Tu código aquí
fFuncion
```

### Construcciones Soportadas
- **Bucles**: `Para i desde 1 hasta N hacer ... fPara`
- **Bucles condicionales**: `Mientras condicion hacer ... fMientras`
- **Condicionales**: `Si condicion Entonces ... Sino ... fSi`
- **Asignaciones**: `variable <- valor`
- **Retorno**: `retornar valor`

## 🔍 Consejos de Uso

### Para Obtener Mejores Resultados:
1. **Usa nombres descriptivos** para funciones y variables
2. **Incluye el parámetro N** para representar el tamaño de entrada
3. **Evita bucles infinitos** - siempre incluye condiciones de parada
4. **Usa comentarios** para explicar partes complejas

### Para Comparaciones Efectivas:
1. **Compara algoritmos similares** (ej: diferentes métodos de ordenamiento)
2. **Observa las gráficas** - las diferencias visuales son muy claras
3. **Prueba con diferentes rangos** de N para ver el comportamiento

## 🐛 Solución de Problemas

### Problema: "Module not found"
**Solución**: 
```bash
pip install -r requirements.txt
```

### Problema: Error al cargar archivos
**Solución**: Verifica que el archivo tenga la sintaxis correcta y esté codificado en UTF-8

### Problema: Gráficas no se muestran
**Solución**: Asegúrate de que matplotlib esté instalado correctamente

### Problema: Análisis incorrecto
**Solución**: Revisa la sintaxis del pseudocódigo - debe seguir exactamente el formato especificado

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta guía
2. Prueba los ejemplos incluidos
3. Verifica que la sintaxis sea correcta
4. Consulta el archivo `ejemplos/README.md` para más detalles

## 🎓 Siguientes Pasos

Una vez que domines lo básico:
1. **Crea tus propios ejemplos** siguiendo la sintaxis
2. **Experimenta con modificaciones** de los ejemplos existentes
3. **Compara diferentes implementaciones** del mismo algoritmo
4. **Explora casos extremos** como algoritmos exponenciales

¡Disfruta explorando la complejidad temporal de los algoritmos!
