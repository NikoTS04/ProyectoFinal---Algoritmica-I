import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import ttkbootstrap as tb
import sys
import os
from tkinter import ttk

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pseudogrammar import tokenizar
from core.parser_estructural import parsear
from core.analizador_complejidad import AnalizadorComplejidad
from core.serializacion import SerializadorAnalisis

class ScrollableFrame(tb.Frame):
    """Frame con scroll vertical para manejar contenido grande"""
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Crear canvas y scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tb.Frame(self.canvas)

        # Configurar el scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Crear ventana en el canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurar el canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar elementos
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind para el scroll con la rueda del ratón
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind para redimensionar
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_mousewheel(self, event):
        """Manejo del scroll con rueda del ratón"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_configure(self, event):
        """Redimensionar el frame interno cuando el canvas cambia de tamaño"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

def crear_pestana_entrada_mejorada(frame, cambiar_a_grafica_callback=None, cambiar_a_comparacion_callback=None):
    """Versión mejorada de la pestaña de entrada con scroll"""
    
    # Crear frame scrollable
    scroll_frame = ScrollableFrame(frame)
    scroll_frame.pack(fill="both", expand=True)
    
    # Usar el frame scrollable como contenedor
    container = scroll_frame.scrollable_frame
    
    # Variable global para almacenar el último resultado del análisis
    ultimo_resultado = None
    serializador = SerializadorAnalisis()
    
    # --- FUNCIONES ---
    def cargar_archivo():
        archivo = tkinter.filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                texto_codigo.delete(1.0, "end")
                texto_codigo.insert("end", contenido)

    def cargar_ejemplo():
        ejemplos_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ejemplos')
        if os.path.exists(ejemplos_dir):
            archivo = tkinter.filedialog.askopenfilename(
                title="Seleccionar ejemplo",
                initialdir=ejemplos_dir,
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if archivo:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    texto_codigo.delete(1.0, "end")
                    texto_codigo.insert("end", contenido)

    def limpiar_texto():
        texto_codigo.delete(1.0, "end")
        texto_resultado.config(state="normal")
        texto_resultado.delete(1.0, "end")
        texto_resultado.config(state="disabled")
        boton_ver_grafica.config(state="disabled")
        boton_comparar.config(state="disabled")
        boton_guardar.config(state="disabled")
        nonlocal ultimo_resultado
        ultimo_resultado = None

    def analizar_codigo():
        codigo = texto_codigo.get(1.0, "end-1c").strip()
        if not codigo:
            tkinter.messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
            return
        
        try:
            # Mostrar mensaje de procesamiento
            texto_resultado.config(state="normal")
            texto_resultado.delete(1.0, "end")
            texto_resultado.insert("end", " Procesando análisis...\n")
            texto_resultado.config(state="disabled")
            container.update()
            
            # Tokenizar y parsear
            tokens = tokenizar(codigo)
            arbol = parsear(tokens)
            analizador = AnalizadorComplejidad(arbol)
            
            # Buscar funciones
            funciones = []
            def encontrar_funciones(nodo):
                if nodo.tipo == 'FUNCION':
                    nombre = nodo.props.get('nombre')
                    if nombre:
                        funciones.append(nombre)
                for hijo in nodo.hijos:
                    encontrar_funciones(hijo)
            
            encontrar_funciones(arbol)
            
            # Analizar
            if funciones:
                resultado = analizador.analizar(funciones[0])
            else:
                resultado = analizador.analizar()
            
            # Mostrar resultado
            texto_resultado.config(state="normal")
            texto_resultado.delete(1.0, "end")
            
            # Resultado exitoso
            texto_resultado.insert("end", " ANÁLISIS COMPLETADO EXITOSAMENTE\n\n")
            texto_resultado.insert("end", f" Función: {resultado.nombre_funcion or 'Código principal'}\n")
            texto_resultado.insert("end", f" Tipo: {'Función recursiva' if resultado.recursivo else 'Función iterativa'}\n")
            texto_resultado.insert("end", f"  T(n) = {resultado.funcion_tiempo.como_str()}\n")
            texto_resultado.insert("end", f" Big O: {resultado.big_o}\n")
            texto_resultado.insert("end", f" Recursivo: {'Sí' if resultado.recursivo else 'No'}\n\n")
            
            # Información adicional
            texto_resultado.insert("end", " Detalles adicionales:\n")
            texto_resultado.insert("end", f"  • Tokens procesados: {len(tokens)}\n")
            texto_resultado.insert("end", f"  • Funciones detectadas: {len(funciones)}\n")
            if funciones:
                texto_resultado.insert("end", f"  • Nombres de funciones: {', '.join(funciones)}\n")
            
            # Interpretación del resultado
            texto_resultado.insert("end", "\n INTERPRETACIÓN:\n")
            big_o = resultado.big_o
            if "O(1)" in big_o:
                texto_resultado.insert("end", " Complejidad constante - Muy eficiente\n")
            elif "log" in big_o.lower():
                texto_resultado.insert("end", " Complejidad logarítmica - Muy eficiente\n")
            elif "O(n)" == big_o:
                texto_resultado.insert("end", " Complejidad lineal - Eficiencia buena\n")
            elif "n**2" in big_o or "n^2" in big_o:
                texto_resultado.insert("end", " Complejidad cuadrática - Cuidado con datos grandes\n")
            elif "2**n" in big_o or "2^n" in big_o:
                texto_resultado.insert("end", " Complejidad exponencial - Solo para datos pequeños\n")
            else:
                texto_resultado.insert("end", " Complejidad personalizada - Analiza caso por caso\n")
            
            texto_resultado.insert("end", "\n💡 Usa las pestañas 'Gráfica' y 'Comparación' para más detalles\n")
            
            texto_resultado.config(state="disabled")
            
            # Habilitar botones
            boton_ver_grafica.config(state="normal")
            boton_comparar.config(state="normal")
            boton_guardar.config(state="normal")
            
            # Guardar resultado
            nonlocal ultimo_resultado
            ultimo_resultado = resultado
            
        except Exception as e:
            # Mostrar error
            texto_resultado.config(state="normal")
            texto_resultado.delete(1.0, "end")
            texto_resultado.insert("end", " Error en el análisis:\n\n")
            texto_resultado.insert("end", f" Detalles: {str(e)}\n\n")
            texto_resultado.insert("end", " Posibles soluciones:\n")
            texto_resultado.insert("end", "• Verifica que el código siga la sintaxis correcta\n")
            texto_resultado.insert("end", "• Asegúrate de que las funciones estén bien definidas\n")
            texto_resultado.insert("end", "• Revisa que los bucles tengan condiciones de parada\n")
            texto_resultado.config(state="disabled")
            
            # Deshabilitar botones
            boton_ver_grafica.config(state="disabled")
            boton_comparar.config(state="disabled")
            boton_guardar.config(state="disabled")

    def guardar_analisis():
        if ultimo_resultado:
            try:
                codigo = texto_codigo.get(1.0, "end-1c")
                archivo_guardado = serializador.guardar_analisis(codigo, ultimo_resultado)
                tkinter.messagebox.showinfo("Guardado", f"Análisis guardado en:\n{archivo_guardado}")
            except Exception as e:
                tkinter.messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def ver_grafica():
        if ultimo_resultado and cambiar_a_grafica_callback:
            cambiar_a_grafica_callback(ultimo_resultado)

    def comparar_algoritmo():
        if ultimo_resultado and cambiar_a_comparacion_callback:
            codigo = texto_codigo.get(1.0, "end-1c")
            cambiar_a_comparacion_callback(ultimo_resultado, codigo)

    # --- ENCABEZADO ---
    encabezado = tb.Frame(container)
    encabezado.pack(fill="x", padx=20, pady=(15, 5))

    etiqueta_codigo = tb.Label(encabezado, text="💻 Ingrese su código aquí:", font=("Segoe UI", 12, "bold"))
    etiqueta_codigo.pack(side="left")

    boton_limpiar = tb.Button(encabezado, text="🧹 Limpiar", command=limpiar_texto, bootstyle="warning-outline")
    boton_limpiar.pack(side="right")

    # --- CAJA DE TEXTO DE ENTRADA ---
    frame_codigo = tb.Frame(container)
    frame_codigo.pack(fill="x", expand=False, padx=20, pady=(0, 10))

    texto_codigo = tb.Text(frame_codigo, wrap="word", font=("Consolas", 11), height=12)
    texto_codigo.pack(side="left", fill="both", expand=True)

    scroll_codigo = tb.Scrollbar(frame_codigo, command=texto_codigo.yview)
    scroll_codigo.pack(side="right", fill="y")
    texto_codigo.config(yscrollcommand=scroll_codigo.set)

    # --- BOTONES DE ACCIÓN ---
    frame_botones = tb.Frame(container)
    frame_botones.pack(pady=10)

    boton_cargar = tb.Button(frame_botones, text="📁 Cargar archivo", command=cargar_archivo, bootstyle="success")
    boton_cargar.pack(side="left", padx=5)

    boton_ejemplo = tb.Button(frame_botones, text="📚 Cargar ejemplo", command=cargar_ejemplo, bootstyle="info-outline")
    boton_ejemplo.pack(side="left", padx=5)

    boton_analizar = tb.Button(frame_botones, text="🔍 Analizar", command=analizar_codigo, bootstyle="primary")
    boton_analizar.pack(side="left", padx=5)

    boton_guardar = tb.Button(frame_botones, text="💾 Guardar", command=guardar_analisis, bootstyle="warning", state="disabled")
    boton_guardar.pack(side="left", padx=5)

    # --- RESULTADO DEL ANÁLISIS ---
    etiqueta_resultado = tb.Label(container, text="📊 Resultado del análisis:", font=("Segoe UI", 12, "bold"))
    etiqueta_resultado.pack(anchor="w", padx=20, pady=(15, 5))

    # Frame con scroll para el área de resultados
    frame_resultado = tb.Frame(container)
    frame_resultado.pack(fill="x", expand=False, padx=20, pady=(0, 10))

    texto_resultado = tb.Text(frame_resultado, wrap="word", font=("Segoe UI", 11), height=12, state="disabled")
    texto_resultado.pack(side="left", fill="both", expand=True)

    scroll_resultado = tb.Scrollbar(frame_resultado, command=texto_resultado.yview)
    scroll_resultado.pack(side="right", fill="y")
    texto_resultado.config(yscrollcommand=scroll_resultado.set)

    # --- BOTONES INFERIORES ---
    frame_inferior = tb.Frame(container)
    frame_inferior.pack(pady=20)

    boton_ver_grafica = tb.Button(frame_inferior, text="📈 Ver gráfica", bootstyle="primary", command=ver_grafica, state="disabled")
    boton_ver_grafica.pack(side="left", padx=10)

    boton_comparar = tb.Button(frame_inferior, text="⚖️ Comparar algoritmo", bootstyle="secondary", command=comparar_algoritmo, state="disabled")
    boton_comparar.pack(side="left", padx=10)

    # --- MENSAJE INICIAL ---
    texto_resultado.config(state="normal")
    texto_resultado.insert("end", " Listo para analizar |  Tip: Carga un ejemplo desde 'Cargar ejemplo'\n\n")
    texto_resultado.insert("end", " Ejemplos disponibles en la carpeta 'ejemplos/'\n")
    texto_resultado.insert("end", " O escribe tu propio pseudocódigo siguiendo la sintaxis del proyecto\n\n")
    texto_resultado.insert("end", " Funcionalidades disponibles:\n")
    texto_resultado.insert("end", "  • Análisis automático de complejidad temporal\n")
    texto_resultado.insert("end", "  • Detección de funciones recursivas\n")
    texto_resultado.insert("end", "  • Visualización gráfica de T(n) vs Big O\n")
    texto_resultado.insert("end", "  • Comparación entre diferentes algoritmos\n")
    texto_resultado.insert("end", "  • Guardado y carga de análisis\n")
    texto_resultado.config(state="disabled")

# Función principal para mantener compatibilidad
def crear_pestana_entrada(frame, cambiar_a_grafica_callback=None, cambiar_a_comparacion_callback=None):
    """Función principal que usa la versión mejorada"""
    return crear_pestana_entrada_mejorada(frame, cambiar_a_grafica_callback, cambiar_a_comparacion_callback)
