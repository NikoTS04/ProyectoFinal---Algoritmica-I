import ttkbootstrap as tb
from ttkbootstrap.constants import *
from entrada import crear_pestana_entrada
from grafica import crear_pestana_grafica
from comparacion import crear_pestana_comparacion

# Crear ventana principal
ventana = tb.Window(themename="flatly")
ventana.title("Analizador de algoritmos")
ventana.geometry("700x900")

# Crear el Notebook
notebook = tb.Notebook(ventana, bootstyle="primary")
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Crear frames para cada pestaña y cargar contenido desde archivos
frame_entrada = tb.Frame(notebook)
frame_grafica = tb.Frame(notebook)
frame_comparacion = tb.Frame(notebook)

#--- Funcion que cambia a la pestaña de gráfica ---
def cambiar_a_grafica():
    notebook.select(frame_grafica)  

crear_pestana_entrada(frame_entrada)
crear_pestana_grafica(frame_grafica)
crear_pestana_comparacion(frame_comparacion)

# Añadir las pestañas al notebook
notebook.add(frame_entrada, text="Entrada")
notebook.add(frame_grafica, text="Gráfica")
notebook.add(frame_comparacion, text="Comparación")

def cambiar_a_grafica():
    notebook.select(1)

# Ejecutar la aplicación
ventana.mainloop()