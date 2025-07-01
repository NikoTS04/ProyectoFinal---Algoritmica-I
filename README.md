# Analizador de Algoritmos en Pseudocódigo

## 📝 Descripción del Proyecto

Este proyecto es un **Analizador Sintáctico de Algoritmos** desarrollado para el curso de Algorítmica I. Permite analizar pseudocódigo y generar su Árbol de Sintaxis Abstracta (AST), facilitando el estudio de la estructura de algoritmos.

## 🎯 Características Principales

- **Tokenizador**: Convierte pseudocódigo en tokens analizables
- **Parser Estructural**: Construye un AST del algoritmo
- **Interfaz Gráfica**: Aplicación intuitiva con ttkbootstrap
- **Análisis de Estructuras**: Soporte para clases, funciones, bucles, condicionales y arreglos
- **Validación**: Detección de errores sintácticos

## 🔧 Componentes del Sistema

### 1. `pseudogrammar.py` - Tokenizador
- Convierte texto a tokens
- Reconoce palabras clave, operadores y símbolos
- Maneja identificadores, números y estructura

### 2. `parser_estructural.py` - Analizador Sintáctico
- Construye el AST
- Valida la estructura del código
- Soporta programación orientada a objetos básica

### 3. `front/` - Interfaz Gráfica
- **frame.py**: Ventana principal con pestañas
- **entrada.py**: Pestaña de ingreso de código
- **grafica.py**: Visualización de resultados
- **comparacion.py**: Comparación de algoritmos

## 📋 Palabras Clave Soportadas

- **Estructuras de Control**: `Si`, `Entonces`, `Sino`, `Mientras`, `Para`, `hacer`
- **Programación Orientada a Objetos**: `Clase`, `Funcion`
- **Operadores**: `<-` (asignación), `<=`, `>=`, `<>`, `+`, `-`, `*`, `/`, `^`
- **Finalizadores**: `fClase`, `fFuncion`, `fSi`, `fMientras`, `fPara`
- **Otros**: `retornar`, `desde`, `hasta`

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
Python 3.12+
```

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
# Ejecutar la interfaz gráfica
cd front
python frame.py

# Probar solo el parser
python parser_estructural.py
```

## 📖 Ejemplos de Uso

### Ejemplo Básico - Búsqueda del Máximo
```
Funcion buscarMaximo(arreglo, tamaño)
    maximo <- arreglo[1]
    Para i desde 2 hasta tamaño hacer
        Si (arreglo[i] > maximo) Entonces
            maximo <- arreglo[i]
        fSi
    fPara
    retornar maximo
fFuncion

datos[5] <- {10, 45, 23, 78, 12}
resultado <- buscarMaximo(datos, 5)
```

### Ejemplo Avanzado - Ordenamiento Burbuja
```
Clase EjemploCompleto
    Funcion ordenarBurbuja(arreglo, n)
        Para i desde 1 hasta n hacer
            Para j desde 1 hasta n-i hacer
                Si (arreglo[j] > arreglo[j+1]) Entonces
                    temp <- arreglo[j]
                    arreglo[j] <- arreglo[j+1]
                    arreglo[j+1] <- temp
                fSi
            fPara
        fPara
    fFuncion
fClase

numeros[10] <- {64, 34, 25, 12, 22, 11, 90, 88, 76, 50}
obj <- EjemploCompleto()
obj.ordenarBurbuja(numeros, 10)
```

## 🧠 Estructuras Soportadas

### Variables y Arreglos
```
x <- 5
arreglo[10] <- {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
matriz[3][4] <- 0
```

### Estructuras de Control
```
Si (condicion) Entonces
    // código
Sino
    // código alternativo
fSi

Mientras (condicion) hacer
    // código del bucle
fMientras

Para variable desde inicio hasta fin hacer
    // código del bucle
fPara
```

### Clases y Funciones
```
Clase MiClase
    Funcion miMetodo(parametro1, parametro2)
        // cuerpo de la función
        retornar resultado
    fFuncion
fClase
```

## 📊 Salida del Analizador

El analizador genera un AST estructurado que muestra:
- Jerarquía de clases y funciones
- Estructura de bucles y condicionales
- Declaraciones y asignaciones de variables
- Llamadas a funciones y métodos
- Información sobre arreglos (tamaño, elementos)

Ejemplo de salida:
```
PROGRAMA
  FUNCION nombre='buscarMaximo' args=[['arreglo'], ['tamaño']]
    ASIGNACION var='maximo' expr=['arreglo', '[', '1', ']']
    PARA var='i' desde='2' hasta='tamaño'
      SI cond=['arreglo', '[', 'i', ']', '>', 'maximo']
        ASIGNACION var='maximo' expr=['arreglo', '[', 'i', ']']
    RETORNAR args=['maximo']
```

## 💡 Casos de Uso

1. **Educativo**: Analizar la estructura de algoritmos para aprendizaje
2. **Validación**: Verificar la sintaxis correcta del pseudocódigo
3. **Visualización**: Entender la jerarquía y flujo de algoritmos
4. **Comparación**: Analizar diferentes implementaciones

## 🔮 Funcionalidades Futuras

- Análisis de complejidad algorítmica
- Generación de gráficos de flujo
- Exportación de diagramas
- Detección de patrones algorítmicos
- Optimización de código

## 🤝 Contribución

Este proyecto fue desarrollado como parte del Proyecto Final de Algorítmica I.
