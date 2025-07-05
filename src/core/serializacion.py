# serializacion.py

import json
import os
from datetime import datetime
from .expresion_simbolica import ExpresionSimbolica

class SerializadorAnalisis:
    """Clase para serializar y deserializar análisis de algoritmos"""
    
    def __init__(self, directorio_guardado="analisis_guardados"):
        self.directorio = directorio_guardado
        if not os.path.exists(directorio_guardado):
            os.makedirs(directorio_guardado)
    
    def guardar_analisis(self, codigo, resultado_analisis, nombre_archivo=None):
        """
        Guarda un análisis completo en un archivo JSON
        
        Args:
            codigo: El código fuente analizado
            resultado_analisis: Instancia de ResultadoAnalisis
            nombre_archivo: Nombre opcional para el archivo (sin extensión)
        
        Returns:
            str: Ruta del archivo guardado
        """
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"analisis_{timestamp}"
        
        # Asegurar que termine en .json
        if not nombre_archivo.endswith('.json'):
            nombre_archivo += '.json'
        
        ruta_archivo = os.path.join(self.directorio, nombre_archivo)
        
        # Preparar datos para serialización
        # Convertir la expresión simbólica de manera más robusta
        import sympy
        expr_dict = {
            "expr_string": str(resultado_analisis.funcion_tiempo.expr),
            "expr_latex": None,  # Para futuras mejoras
            "variables": [str(sym) for sym in resultado_analisis.funcion_tiempo.expr.free_symbols]
        }
        
        datos = {
            "codigo": codigo,
            "nombre_funcion": resultado_analisis.nombre_funcion,
            "funcion_tiempo": expr_dict,
            "big_o": resultado_analisis.big_o,
            "recursivo": resultado_analisis.recursivo,
            "fecha_creacion": datetime.now().isoformat(),
            "version": "2.0"  # Incrementar versión para nuevo formato
        }
        
        # Guardar archivo
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        return ruta_archivo
    
    def cargar_analisis(self, ruta_archivo):
        """
        Carga un análisis desde un archivo JSON
        
        Args:
            ruta_archivo: Ruta al archivo JSON
        
        Returns:
            dict: Diccionario con el código y resultado del análisis
        """
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Reconstruir ExpresionSimbolica
        from .analizador_complejidad import ResultadoAnalisis
        import sympy
        
        try:
            # Detectar versión del archivo
            version = datos.get("version", "1.0")
            
            if version == "1.0":
                # Formato anterior (string directo)
                expr_string = datos["funcion_tiempo"]
            else:
                # Formato nuevo (diccionario)
                expr_string = datos["funcion_tiempo"]["expr_string"]
            
            # Intentar convertir la cadena de vuelta a expresión simbólica
            # Crear los símbolos necesarios primero
            N = sympy.Symbol('N')
            n = sympy.Symbol('n')
            
            # Crear un namespace local para sympify con funciones comunes
            local_dict = {
                'N': N, 'n': n, 
                'E': sympy.E, 
                'log': sympy.log,
                'exp': sympy.exp,
                'pow': sympy.Pow,
                'sqrt': sympy.sqrt,
                'sin': sympy.sin,
                'cos': sympy.cos,
                'pi': sympy.pi
            }
            
            # Limpiar la cadena de expresión de caracteres problemáticos
            expr_clean = expr_string.replace('**', '^').replace('^', '**')
            
            # Convertir la expresión
            expr_sympy = sympy.sympify(expr_clean, locals=local_dict)
            funcion_tiempo = ExpresionSimbolica(expr_sympy)
            
        except Exception as e:
            # Si hay error en la conversión, crear una expresión simple
            print(f"Advertencia: Error al cargar expresión '{expr_string}': {e}")
            try:
                # Intentar crear una expresión simple basada en el Big O
                big_o = datos.get("big_o", "O(1)")
                if "2^" in big_o or "2**" in big_o:
                    # Exponencial
                    N = sympy.Symbol('N')
                    expr_sympy = 2**N
                elif "n**2" in big_o or "n^2" in big_o:
                    # Cuadrático
                    N = sympy.Symbol('N')
                    expr_sympy = N**2
                elif "n" in big_o.lower():
                    # Lineal
                    N = sympy.Symbol('N')
                    expr_sympy = N
                else:
                    # Constante
                    expr_sympy = sympy.Integer(1)
                
                funcion_tiempo = ExpresionSimbolica(expr_sympy)
                print(f"Usando expresión de fallback basada en {big_o}: {expr_sympy}")
                
            except Exception as e2:
                print(f"Error en fallback: {e2}")
                # Último recurso: expresión constante
                funcion_tiempo = ExpresionSimbolica.constante(1)
        
        resultado = ResultadoAnalisis(
            funcion_tiempo=funcion_tiempo,
            big_o=datos["big_o"],
            recursivo=datos["recursivo"],
            nombre_funcion=datos["nombre_funcion"]
        )
        
        return {
            "codigo": datos["codigo"],
            "resultado": resultado,
            "fecha_creacion": datos.get("fecha_creacion"),
            "version": datos.get("version", "1.0")
        }
    
    def listar_analisis_guardados(self):
        """
        Lista todos los análisis guardados en el directorio
        
        Returns:
            list: Lista de diccionarios con información de los archivos
        """
        archivos = []
        for archivo in os.listdir(self.directorio):
            if archivo.endswith('.json'):
                ruta_completa = os.path.join(self.directorio, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    
                    archivos.append({
                        "archivo": archivo,
                        "ruta": ruta_completa,
                        "nombre_funcion": datos.get("nombre_funcion", "Sin nombre"),
                        "fecha_creacion": datos.get("fecha_creacion", "Desconocida"),
                        "big_o": datos.get("big_o", "Desconocido")
                    })
                except Exception:
                    continue  # Ignorar archivos corruptos
        
        # Ordenar por fecha de creación (más recientes primero)
        archivos.sort(key=lambda x: x["fecha_creacion"], reverse=True)
        return archivos
    
    def eliminar_analisis(self, ruta_archivo):
        """
        Elimina un archivo de análisis
        
        Args:
            ruta_archivo: Ruta al archivo a eliminar
        
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            os.remove(ruta_archivo)
            return True
        except Exception:
            return False
