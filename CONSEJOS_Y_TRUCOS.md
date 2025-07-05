# Consejos y Trucos - Analizador de Complejidad Temporal

## 🎯 Consejos para Obtener Mejores Resultados

### 📝 Escribiendo Pseudocódigo Efectivo

1. **Usa nombres descriptivos**
   ```
   ✅ Bueno: Funcion busquedaBinaria(N)
   ❌ Malo:  Funcion f(x)
   ```

2. **Incluye el parámetro N**
   ```
   ✅ Bueno: Para i desde 1 hasta N hacer
   ❌ Malo:  Para i desde 1 hasta 100 hacer
   ```

3. **Estructura clara**
   ```
   Funcion nombreFuncion(N)
       // Variables locales
       variable <- valor
       
       // Lógica principal
       Para i desde 1 hasta N hacer
           // operaciones
       fPara
       
       retornar resultado
   fFuncion
   ```

### 🔍 Interpretando Resultados

**Complejidades Comunes:**
- **O(1)** → Constante: Acceso a array, asignaciones simples
- **O(log n)** → Logarítmica: Búsqueda binaria, divide y vencerás
- **O(n)** → Lineal: Búsqueda secuencial, recorrido simple
- **O(n log n)** → Linearítmica: Mergesort, Heapsort
- **O(n²)** → Cuadrática: Burbuja, bucles anidados
- **O(2ⁿ)** → Exponencial: Fibonacci recursivo, backtracking

### 📊 Usando las Gráficas

1. **Pestaña Gráfica:**
   - Verde: Tu función T(n)
   - Rojo: Big O teórico
   - Si están muy separadas, revisa el análisis

2. **Pestaña Comparación:**
   - Carga dos algoritmos diferentes
   - Observa cuál crece más lento
   - Perfecto para comparar implementaciones

### 💾 Gestión de Análisis

**Guardar efectivamente:**
- Usa nombres descriptivos: "busqueda_binaria_optimizada"
- Guarda antes de modificar el código
- Aprovecha la comparación con análisis guardados

## ⚡ Atajos y Trucos

### 🖥️ Interfaz Gráfica
- **Ctrl+A**: Seleccionar todo el código
- **Ctrl+C/V**: Copiar y pegar como siempre
- **Tab entre pestañas**: Usa mouse o flechas para navegar

### 💻 Línea de Comandos
```bash
# Análisis básico
python main.py --cli archivo.txt

# Análisis detallado
python main.py --cli archivo.txt --verbose

# Análisis y guardado automático
python main.py --cli archivo.txt --save

# Ver ayuda completa
python main.py --help

# Listar ejemplos disponibles
python main.py --ejemplos

# Probar todos los ejemplos
python probar_ejemplos.py

# Validar que todo funcione
python validar_sistema.py
```

### 🚀 Flujo de Trabajo Recomendado

1. **Para Aprender:**
   ```
   1. Ejecuta: python main.py --ejemplos
   2. Prueba ejemplos simples primero
   3. Compara algoritmos similares
   4. Experimenta modificando ejemplos
   ```

2. **Para Desarrollo:**
   ```
   1. Escribe tu algoritmo
   2. Analiza con --verbose
   3. Guarda con --save
   4. Compara con implementaciones conocidas
   ```

3. **Para Enseñanza:**
   ```
   1. Usa ejemplos predefinidos
   2. Ejecuta probar_ejemplos.py para demostrar variedad
   3. Muestra comparaciones visuales
   4. Deja que los estudiantes experimenten
   ```

## 🐛 Solución de Problemas Comunes

### ❌ "Error en el análisis"
**Causas comunes:**
- Sintaxis incorrecta del pseudocódigo
- Bucles sin condición de parada
- Funciones mal definidas

**Soluciones:**
1. Revisa la sintaxis básica
2. Compara con ejemplos funcionando
3. Usa --verbose para más detalles

### ❌ "Complejidad incorrecta"
**Posibles razones:**
- El analizador tiene limitaciones conocidas
- Algoritmo muy complejo para detección automática
- Lógica no estándar

**Soluciones:**
1. Simplifica el código
2. Compara con algoritmos conocidos
3. Consulta la documentación de limitaciones

### ❌ "Gráficas no se muestran"
**Verificaciones:**
1. `python validar_sistema.py`
2. Reinstalar matplotlib: `pip install matplotlib --upgrade`
3. Reiniciar la aplicación

### ❌ "Archivo no encontrado"
**Soluciones:**
1. Verifica la ruta completa
2. Usa comillas si hay espacios: `"mi archivo.txt"`
3. Asegúrate de que el archivo exista

## 💡 Tips Avanzados

### 🔬 Análisis Profundo
1. **Combina métodos**: CLI para análisis rápido, GUI para visualización
2. **Usa verbose**: Siempre con `--verbose` para entender qué pasa
3. **Experimenta**: Modifica ejemplos para ver cómo cambia la complejidad

### 📈 Optimización
1. **Compara implementaciones**: Recursiva vs iterativa
2. **Detecta patrones**: Bucles anidados = probable O(n²)
3. **Considera casos base**: Recursión siempre necesita casos base

### 🎓 Aprendizaje
1. **Empieza simple**: O(1) → O(n) → O(n²) → O(2ⁿ)
2. **Visualiza siempre**: Las gráficas muestran diferencias dramáticas
3. **Compara constantemente**: Es la mejor forma de entender eficiencia

## 📚 Recursos Adicionales

- **Ejemplos incluidos**: 15+ algoritmos listos para usar
- **Documentación**: README.md y GUIA_USUARIO.md
- **Validación**: validar_sistema.py para verificar instalación
- **Testing**: probar_ejemplos.py para verificar funcionamiento

¡Disfruta analizando algoritmos! 🚀
