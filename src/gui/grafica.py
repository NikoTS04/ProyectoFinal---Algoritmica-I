import ttkbootstrap as tb
import matplotlib
matplotlib.use('TkAgg')  # Configurar backend antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import sympy
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def crear_pestana_grafica(frame):
    # Variable global para almacenar el resultado actual
    resultado_actual = None
    
    def actualizar_grafica(resultado_analisis=None):
        """Actualiza la gráfica con un nuevo resultado de análisis"""
        nonlocal resultado_actual
        if resultado_analisis:
            resultado_actual = resultado_analisis
            mostrar_grafica()
    
    def mostrar_grafica():
        """Muestra la gráfica del análisis actual"""
        if resultado_actual is None:
            # Mostrar mensaje cuando no hay datos
            etiqueta_info.config(text="No hay análisis para mostrar. Analice código en la pestaña 'Entrada' primero.")
            return
        
        # Limpiar frame anterior si existe
        for widget in frame_grafica.winfo_children():
            widget.destroy()
        
        try:
            # Crear figura de matplotlib embebida
            fig = Figure(figsize=(12, 5), dpi=100)
            ax1, ax2 = fig.subplots(1, 2)
            fig.suptitle(f'Análisis de Complejidad - {resultado_actual.nombre_funcion or "Código"}', fontsize=14)
            
            # Configurar rango de valores
            n_values = np.arange(1, 21)
            
            # Graficar función de tiempo T(n)
            t_values = []
            expr = resultado_actual.funcion_tiempo.expr
            
            for n in n_values:
                try:
                    # Evaluar la expresión simbólica usando Symbol
                    val = expr.subs(sympy.Symbol('N'), n)
                    if hasattr(val, 'is_number') and val.is_number:
                        t_values.append(float(val))
                    elif hasattr(val, 'evalf'):
                        # Si la expresión contiene variables no substituidas, evaluar numéricamente
                        result = float(val.evalf())
                        # Limitar valores muy grandes para visualización
                        t_values.append(min(result, 1e6))
                    else:
                        t_values.append(float(val))
                except Exception as e:
                    # Fallback basado en Big O
                    big_o = resultado_actual.big_o
                    if "2^" in big_o or "2**" in big_o:
                        t_values.append(min(2**n, 1e6))
                    elif "n**2" in big_o or "n^2" in big_o:
                        t_values.append(n**2)
                    elif "n" in big_o.lower():
                        t_values.append(n)
                    else:
                        t_values.append(1)
            
            ax1.plot(n_values, t_values, 'b-o', linewidth=2, markersize=6, label=f'T(n) = {resultado_actual.funcion_tiempo.como_str()}')
            ax1.set_xlabel('Tamaño de entrada (n)')
            ax1.set_ylabel('Tiempo de ejecución')
            ax1.set_title('Función de Tiempo T(n)')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Graficar comparación con Big O
            big_o_str = resultado_actual.big_o.replace('O(', '').replace(')', '')
            
            # Generar función Big O para comparación
            big_o_values = []
            try:
                # Preparar el string de Big O para sympy
                big_o_clean = big_o_str.replace('**', '^').replace('^', '**')
                N = sympy.Symbol('N')
                local_dict = {'N': N, 'n': N, 'log': sympy.log}
                big_o_expr = sympy.sympify(big_o_clean, locals=local_dict)
                
                for n in n_values:
                    val = big_o_expr.subs(N, n)
                    if hasattr(val, 'is_number') and val.is_number:
                        big_o_values.append(float(val))
                    elif hasattr(val, 'evalf'):
                        result = float(val.evalf())
                        big_o_values.append(min(result, 1e6))
                    else:
                        big_o_values.append(float(val))
            except Exception as e:
                # Fallback para casos complejos
                if "2^" in big_o_str or "2**" in big_o_str:
                    big_o_values = [min(2**n, 1e6) for n in n_values]
                elif "n**2" in big_o_str or "n^2" in big_o_str:
                    big_o_values = [n**2 for n in n_values]
                elif "n" in big_o_str.lower():
                    big_o_values = [n for n in n_values]
                else:
                    big_o_values = [1 for n in n_values]
            
            ax2.plot(n_values, t_values, 'b-o', linewidth=2, markersize=6, label=f'T(n) = {resultado_actual.funcion_tiempo.como_str()}')
            ax2.plot(n_values, big_o_values, 'r--', linewidth=2, label=f'Big O = {resultado_actual.big_o}')
            ax2.set_xlabel('Tamaño de entrada (n)')
            ax2.set_ylabel('Tiempo de ejecución')
            ax2.set_title('Comparación T(n) vs Big O')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            fig.tight_layout()
            
            # Integrar matplotlib con tkinter
            canvas = FigureCanvasTkAgg(fig, frame_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Agregar barra de herramientas de navegación
            toolbar_frame = tb.Frame(frame_grafica)
            toolbar_frame.pack(fill="x")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Actualizar etiqueta de información
            info_text = f"Función: {resultado_actual.nombre_funcion or 'Código principal'}\n"
            info_text += f"T(n) = {resultado_actual.funcion_tiempo.como_str()}\n"
            info_text += f"Big O: {resultado_actual.big_o}"
            if resultado_actual.recursivo:
                info_text += "\nTipo: Función recursiva"
            
            etiqueta_info.config(text=info_text)
            
        except Exception as e:
            etiqueta_info.config(text=f"Error al generar gráfica: {str(e)}")
    
    def exportar_grafica():
        """Exporta la gráfica actual como imagen"""
        if resultado_actual is None:
            return
        
        import tkinter.filedialog
        archivo = tkinter.filedialog.asksaveasfilename(
            title="Guardar gráfica",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("PDF", "*.pdf")]
        )
        
        if archivo:
            try:
                # Obtener la figura actual del canvas
                for widget in frame_grafica.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.figure.savefig(archivo, dpi=300, bbox_inches='tight')
                        break
                
                import tkinter.messagebox
                tkinter.messagebox.showinfo("Éxito", f"Gráfica guardada en: {archivo}")
            except Exception as e:
                import tkinter.messagebox
                tkinter.messagebox.showerror("Error", f"No se pudo guardar la gráfica: {str(e)}")
    
    # --- INTERFAZ GRÁFICA ---
    
    # Frame superior con información
    frame_info = tb.Frame(frame)
    frame_info.pack(fill="x", padx=10, pady=5)
    
    etiqueta_titulo = tb.Label(frame_info, text="Visualización de Complejidad Temporal", font=("Segoe UI", 14, "bold"))
    etiqueta_titulo.pack(side="left")
    
    boton_exportar = tb.Button(frame_info, text="Exportar gráfica", command=exportar_grafica, bootstyle="success-outline")
    boton_exportar.pack(side="right")
    
    # Etiqueta de información del análisis
    etiqueta_info = tb.Label(frame, text="No hay análisis para mostrar. Analice código en la pestaña 'Entrada' primero.", 
                           font=("Segoe UI", 11), wraplength=600, justify="left")
    etiqueta_info.pack(padx=10, pady=10)
    
    # Frame para la gráfica
    frame_grafica = tb.Frame(frame)
    frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Exponer función para uso externo
    frame.actualizar_grafica = actualizar_grafica
