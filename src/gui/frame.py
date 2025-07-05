import ttkbootstrap as tb
from ttkbootstrap.constants import *
from .entrada import crear_pestana_entrada
from .grafica import crear_pestana_grafica
from .comparacion import crear_pestana_comparacion

# Crear ventana principal
ventana = tb.Window(themename="flatly")
ventana.title("Analizador de algoritmos")
ventana.geometry("800x700")

# Crear el Notebook
notebook = tb.Notebook(ventana, bootstyle="primary")
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Crear frames para cada pestaña
frame_entrada = tb.Frame(notebook)
frame_grafica = tb.Frame(notebook)
frame_comparacion = tb.Frame(notebook)

# Variables globales para comunicación entre pestañas
resultado_actual = None

# Función que cambia a la pestaña de gráfica y actualiza con resultado
def cambiar_a_grafica(resultado_analisis=None):
    global resultado_actual
    if resultado_analisis:
        resultado_actual = resultado_analisis
        # Actualizar gráfica si la función existe
        if hasattr(frame_grafica, 'actualizar_grafica'):
            frame_grafica.actualizar_grafica(resultado_analisis)
    notebook.select(frame_grafica)

# Función que cambia a la pestaña de comparación
def cambiar_a_comparacion(resultado_analisis=None, codigo=""):
    if resultado_analisis and hasattr(frame_comparacion, 'establecer_algoritmo1'):
        frame_comparacion.establecer_algoritmo1(resultado_analisis, codigo)
    notebook.select(frame_comparacion)

# Crear contenido de las pestañas
crear_pestana_entrada(frame_entrada, cambiar_a_grafica, cambiar_a_comparacion)
crear_pestana_grafica(frame_grafica)
crear_pestana_comparacion(frame_comparacion)

# Añadir las pestañas al notebook
notebook.add(frame_entrada, text="Entrada")
notebook.add(frame_grafica, text="Gráfica")
notebook.add(frame_comparacion, text="Comparación")

# Ejecutar la aplicación
ventana.mainloop()