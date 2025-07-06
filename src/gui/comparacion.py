import ttkbootstrap as tb
import tkinter.filedialog
import tkinter.messagebox
import matplotlib
matplotlib.use('TkAgg')  # Configurar backend antes de importar pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import sympy
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pseudogrammar import tokenizar
from core.parser_estructural import parsear
from core.analizador_complejidad import AnalizadorComplejidad
from core.serializacion import SerializadorAnalisis

def crear_pestana_comparacion(frame):
    # Variables para almacenar los algoritmos a comparar
    algoritmo1 = None
    algoritmo2 = None
    serializador = SerializadorAnalisis()
    
    def cargar_codigo_nuevo():
        """Permite cargar un segundo algoritmo escribiendo código"""
        ventana_codigo = tb.Toplevel()
        ventana_codigo.title("Cargar segundo algoritmo")
        ventana_codigo.geometry("600x500")
        
        # Área de texto para código
        etiqueta = tb.Label(ventana_codigo, text="Ingrese el código del segundo algoritmo:", font=("Segoe UI", 11, "bold"))
        etiqueta.pack(padx=10, pady=5)
        
        texto_codigo = tb.Text(ventana_codigo, wrap="word", font=("Segoe UI", 11), height=15)
        texto_codigo.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Botones
        frame_botones = tb.Frame(ventana_codigo)
        frame_botones.pack(pady=10)
        
        def analizar_segundo():
            codigo = texto_codigo.get(1.0, "end-1c").strip()
            if not codigo:
                tkinter.messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
                return
            
            try:
                tokens = tokenizar(codigo)
                arbol = parsear(tokens)
                analizador = AnalizadorComplejidad(arbol)
                
                # Buscar funciones
                funciones = encontrar_funciones(arbol)
                if funciones:
                    resultado = analizador.analizar(funciones[0])
                else:
                    resultado = analizador.analizar()
                
                nonlocal algoritmo2
                algoritmo2 = {
                    "codigo": codigo,
                    "resultado": resultado,
                    "nombre": resultado.nombre_funcion or "Algoritmo 2"
                }
                
                actualizar_interfaz()
                ventana_codigo.destroy()
                tkinter.messagebox.showinfo("Éxito", "Segundo algoritmo cargado correctamente")
                
            except Exception as e:
                tkinter.messagebox.showerror("Error", f"Error al analizar el código:\n{str(e)}")
        
        def cancelar():
            ventana_codigo.destroy()
        
        boton_analizar = tb.Button(frame_botones, text="Analizar", command=analizar_segundo, bootstyle="info")
        boton_analizar.pack(side="left", padx=5)
        
        boton_cancelar = tb.Button(frame_botones, text="Cancelar", command=cancelar, bootstyle="secondary")
        boton_cancelar.pack(side="left", padx=5)
    
    def cargar_desde_archivo_txt():
        """Carga un algoritmo desde un archivo .txt"""
        archivo = tkinter.filedialog.askopenfilename(
            title="Seleccionar archivo de pseudocódigo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            # Analizar el código
            tokens = tokenizar(codigo)
            arbol = parsear(tokens)
            analizador = AnalizadorComplejidad(arbol)
            
            # Buscar funciones
            funciones = encontrar_funciones(arbol)
            if funciones:
                resultado = analizador.analizar(funciones[0])
            else:
                resultado = analizador.analizar()
            
            nonlocal algoritmo2
            algoritmo2 = {
                "codigo": codigo,
                "resultado": resultado,
                "nombre": resultado.nombre_funcion or os.path.basename(archivo).replace('.txt', '')
            }
            
            actualizar_interfaz()
            tkinter.messagebox.showinfo("Éxito", f"Algoritmo cargado desde {os.path.basename(archivo)}")
            
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")

    def cargar_desde_archivo():
        """Carga un algoritmo desde un archivo guardado"""
        archivos = serializador.listar_analisis_guardados()
        
        if not archivos:
            tkinter.messagebox.showinfo("Información", "No hay análisis guardados disponibles")
            return
        
        # Crear ventana de selección
        ventana_seleccion = tb.Toplevel()
        ventana_seleccion.title("Seleccionar algoritmo guardado")
        ventana_seleccion.geometry("500x400")
        
        etiqueta = tb.Label(ventana_seleccion, text="Seleccione un análisis guardado:", font=("Segoe UI", 11, "bold"))
        etiqueta.pack(padx=10, pady=5)
        
        # Lista de archivos
        frame_lista = tb.Frame(ventana_seleccion)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        listbox = tb.Treeview(frame_lista, columns=("Función", "Big O", "Fecha"), show="headings", height=10)
        listbox.heading("Función", text="Función")
        listbox.heading("Big O", text="Big O")
        listbox.heading("Fecha", text="Fecha")
        
        # Scrollbar
        scrollbar = tb.Scrollbar(frame_lista, orient="vertical", command=listbox.yview)
        listbox.configure(yscroll=scrollbar.set)
        
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Llenar lista
        for archivo in archivos:
            fecha = archivo["fecha_creacion"][:10] if len(archivo["fecha_creacion"]) > 10 else archivo["fecha_creacion"]
            listbox.insert("", "end", values=(archivo["nombre_funcion"], archivo["big_o"], fecha), tags=(archivo["ruta"],))
        
        # Botones
        frame_botones = tb.Frame(ventana_seleccion)
        frame_botones.pack(pady=10)
        
        def seleccionar_archivo():
            seleccion = listbox.selection()
            if not seleccion:
                tkinter.messagebox.showwarning("Advertencia", "Por favor seleccione un archivo")
                return
            
            item = listbox.item(seleccion[0])
            ruta_archivo = item["tags"][0]
            
            try:
                datos = serializador.cargar_analisis(ruta_archivo)
                nonlocal algoritmo2
                algoritmo2 = {
                    "codigo": datos["codigo"],
                    "resultado": datos["resultado"],
                    "nombre": datos["resultado"].nombre_funcion or "Algoritmo guardado"
                }
                
                actualizar_interfaz()
                ventana_seleccion.destroy()
                tkinter.messagebox.showinfo("Éxito", "Algoritmo cargado correctamente")
                
            except Exception as e:
                tkinter.messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
        
        def cancelar():
            ventana_seleccion.destroy()
        
        boton_seleccionar = tb.Button(frame_botones, text="Seleccionar", command=seleccionar_archivo, bootstyle="info")
        boton_seleccionar.pack(side="left", padx=5)
        
        boton_cancelar = tb.Button(frame_botones, text="Cancelar", command=cancelar, bootstyle="secondary")
        boton_cancelar.pack(side="left", padx=5)
    
    def encontrar_funciones(nodo):
        """Encuentra todas las funciones definidas en el árbol"""
        funciones = []
        if nodo.tipo == 'FUNCION':
            nombre = nodo.props.get('nombre')
            if nombre:
                funciones.append(nombre)
        for hijo in nodo.hijos:
            funciones.extend(encontrar_funciones(hijo))
        return funciones
    
    def comparar_algoritmos():
        """Genera la comparación visual entre ambos algoritmos"""
        if algoritmo1 is None or algoritmo2 is None:
            tkinter.messagebox.showwarning("Advertencia", "Necesita cargar dos algoritmos para comparar")
            return

        # Limpiar frame de gráfica
        for widget in frame_grafica.winfo_children():
            widget.destroy()

        try:
            # Crear figura de matplotlib embebida
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            fig.suptitle('Comparación de Algoritmos', fontsize=14)

            # Configurar rango de valores
            n_values = np.arange(1, 21)

            # Evaluar algoritmo 1
            t1_values = []
            expr1 = algoritmo1["resultado"].funcion_tiempo.expr
            for n in n_values:
                try:
                    # Usar sympy para evaluación segura
                    val = expr1.subs(sympy.Symbol('N'), n)
                    # Asegurar que el resultado sea numérico
                    if hasattr(val, 'evalf'):
                        result = float(val.evalf())
                    else:
                        result = float(val)
                    # Limitar valores muy grandes para visualización
                    t1_values.append(min(result, 1e6))
                except Exception as e:
                    # Fallback basado en Big O
                    big_o = algoritmo1["resultado"].big_o
                    if "2^" in big_o or "2**" in big_o:
                        t1_values.append(min(2**n, 1e6))
                    elif "n**2" in big_o or "n^2" in big_o:
                        t1_values.append(n**2)
                    elif "n" in big_o.lower():
                        t1_values.append(n)
                    else:
                        t1_values.append(1)

            # Evaluar algoritmo 2
            t2_values = []
            expr2 = algoritmo2["resultado"].funcion_tiempo.expr
            for n in n_values:
                try:
                    # Usar sympy para evaluación segura
                    val = expr2.subs(sympy.Symbol('N'), n)
                    # Asegurar que el resultado sea numérico
                    if hasattr(val, 'evalf'):
                        result = float(val.evalf())
                    else:
                        result = float(val)
                    # Limitar valores muy grandes para visualización
                    t2_values.append(min(result, 1e6))
                except Exception as e:
                    # Fallback basado en Big O
                    big_o = algoritmo2["resultado"].big_o
                    if "2^" in big_o or "2**" in big_o:
                        t2_values.append(min(2**n, 1e6))
                    elif "n**2" in big_o or "n^2" in big_o:
                        t2_values.append(n**2)
                    elif "n" in big_o.lower():
                        t2_values.append(n)
                    else:
                        t2_values.append(1)
            
            # Graficar ambos algoritmos
            ax.plot(n_values, t1_values, 'b-o', linewidth=2, markersize=6, 
                   label=f'{algoritmo1["nombre"]}: {algoritmo1["resultado"].big_o}')
            ax.plot(n_values, t2_values, 'r-s', linewidth=2, markersize=6, 
                   label=f'{algoritmo2["nombre"]}: {algoritmo2["resultado"].big_o}')
            
            ax.set_xlabel('Tamaño de entrada (n)')
            ax.set_ylabel('Tiempo de ejecución')
            ax.set_title('Comparación de Complejidad Temporal')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            fig.tight_layout()
            
            # Integrar con tkinter
            canvas = FigureCanvasTkAgg(fig, frame_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Agregar barra de herramientas de navegación
            toolbar_frame = tb.Frame(frame_grafica)
            toolbar_frame.pack(fill="x")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Actualizar análisis comparativo
            actualizar_analisis_comparativo()
            
        except Exception as e:
            etiqueta_analisis.config(text=f"Error al generar comparación: {str(e)}")
    
    def actualizar_analisis_comparativo():
        """Actualiza el texto del análisis comparativo"""
        if algoritmo1 is None or algoritmo2 is None:
            return
        
        texto = "=== ANÁLISIS COMPARATIVO ===\n\n"
        
        # Información de algoritmo 1
        texto += f"Algoritmo 1: {algoritmo1['nombre']}\n"
        try:
            texto += f"  T(n) = {algoritmo1['resultado'].funcion_tiempo.como_str()}\n"
        except:
            texto += f"  T(n) = {str(algoritmo1['resultado'].funcion_tiempo.expr)}\n"
        texto += f"  Big O: {algoritmo1['resultado'].big_o}\n\n"
        
        # Información de algoritmo 2
        texto += f"Algoritmo 2: {algoritmo2['nombre']}\n"
        try:
            texto += f"  T(n) = {algoritmo2['resultado'].funcion_tiempo.como_str()}\n"
        except:
            texto += f"  T(n) = {str(algoritmo2['resultado'].funcion_tiempo.expr)}\n"
        texto += f"  Big O: {algoritmo2['resultado'].big_o}\n\n"
        
        # Comparación simple
        big_o1 = algoritmo1['resultado'].big_o
        big_o2 = algoritmo2['resultado'].big_o
        
        texto += "=== CONCLUSIÓN ===\n"
        
        # Análisis más detallado de complejidades
        def extraer_complejidad(big_o):
            """Extrae el tipo de complejidad de la notación Big O"""
            if "2^" in big_o or "2**" in big_o:
                return "exponencial"
            elif "n**3" in big_o or "n^3" in big_o:
                return "cubica"
            elif "n**2" in big_o or "n^2" in big_o:
                return "cuadratica"
            elif "n*log" in big_o or "nlog" in big_o:
                return "linearitmica"
            elif "log" in big_o:
                return "logaritmica"
            elif "n" in big_o.lower() and "log" not in big_o:
                return "lineal"
            else:
                return "constante"
        
        comp1 = extraer_complejidad(big_o1)
        comp2 = extraer_complejidad(big_o2)
        
        # Orden de eficiencia (más eficiente a menos eficiente)
        orden_eficiencia = ["constante", "logaritmica", "lineal", "linearitmica", "cuadratica", "cubica", "exponencial"]
        
        pos1 = orden_eficiencia.index(comp1) if comp1 in orden_eficiencia else len(orden_eficiencia)
        pos2 = orden_eficiencia.index(comp2) if comp2 in orden_eficiencia else len(orden_eficiencia)
        
        if pos1 < pos2:
            texto += f"El {algoritmo1['nombre']} es más eficiente ({comp1} vs {comp2})"
        elif pos2 < pos1:
            texto += f"El {algoritmo2['nombre']} es más eficiente ({comp2} vs {comp1})"
        else:
            texto += f"Ambos algoritmos tienen complejidad similar ({comp1})"
        
        etiqueta_analisis.config(text=texto)
    
    def actualizar_interfaz():
        """Actualiza la interfaz con el estado actual de los algoritmos"""
        if algoritmo1:
            etiqueta_algo1.config(text=f"Algoritmo 1: {algoritmo1['nombre']} - {algoritmo1['resultado'].big_o}")
        else:
            etiqueta_algo1.config(text="Algoritmo 1: No cargado")
        
        if algoritmo2:
            etiqueta_algo2.config(text=f"Algoritmo 2: {algoritmo2['nombre']} - {algoritmo2['resultado'].big_o}")
        else:
            etiqueta_algo2.config(text="Algoritmo 2: No cargado")
        
        # Habilitar botón de comparar si ambos están cargados
        if algoritmo1 and algoritmo2:
            boton_comparar.config(state="normal")
        else:
            boton_comparar.config(state="disabled")
    
    def establecer_algoritmo1(resultado_analisis, codigo="", nombre=""):
        """Función para establecer el primer algoritmo desde otra pestaña"""
        nonlocal algoritmo1
        algoritmo1 = {
            "codigo": codigo,
            "resultado": resultado_analisis,
            "nombre": nombre or resultado_analisis.nombre_funcion or "Algoritmo 1"
        }
        actualizar_interfaz()
    
    # --- INTERFAZ GRÁFICA ---
    
    # Título
    etiqueta_titulo = tb.Label(frame, text="Comparación de Algoritmos", font=("Segoe UI", 14, "bold"))
    etiqueta_titulo.pack(padx=10, pady=10)
    
    # Estado de algoritmos
    frame_estado = tb.Frame(frame)
    frame_estado.pack(fill="x", padx=10, pady=5)
    
    etiqueta_algo1 = tb.Label(frame_estado, text="Algoritmo 1: No cargado", font=("Segoe UI", 10))
    etiqueta_algo1.pack(anchor="w")
    
    etiqueta_algo2 = tb.Label(frame_estado, text="Algoritmo 2: No cargado", font=("Segoe UI", 10))
    etiqueta_algo2.pack(anchor="w")
    
    # Botones de carga
    frame_botones = tb.Frame(frame)
    frame_botones.pack(pady=10)
    
    boton_nuevo = tb.Button(frame_botones, text="📝 Cargar código nuevo", command=cargar_codigo_nuevo, bootstyle="info")
    boton_nuevo.pack(side="left", padx=5)
    
    boton_archivo_txt = tb.Button(frame_botones, text="📁 Cargar desde archivo .txt", command=cargar_desde_archivo_txt, bootstyle="warning")
    boton_archivo_txt.pack(side="left", padx=5)
    
    boton_archivo = tb.Button(frame_botones, text="💾 Cargar desde archivo guardado", command=cargar_desde_archivo, bootstyle="success")
    boton_archivo.pack(side="left", padx=5)
    
    boton_comparar = tb.Button(frame_botones, text="🔍 Comparar", command=comparar_algoritmos, bootstyle="primary", state="disabled")
    boton_comparar.pack(side="left", padx=5)
    
    # Frame para gráfica
    frame_grafica = tb.Frame(frame)
    frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Análisis comparativo
    etiqueta_analisis = tb.Label(frame, text="Cargue dos algoritmos para ver el análisis comparativo", 
                               font=("Segoe UI", 10), wraplength=600, justify="left")
    etiqueta_analisis.pack(padx=10, pady=5)
    
    # Exponer función para uso externo
    frame.establecer_algoritmo1 = establecer_algoritmo1
    
    actualizar_interfaz()
