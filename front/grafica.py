import ttkbootstrap as tb

def crear_pestana_grafica(frame):
    etiqueta = tb.Label(frame, text="Aquí se mostrará la gráfica del análisis.", font=("Segoe UI", 12))
    etiqueta.pack(padx=10, pady=20)

    # Dummy gráfico (puedes usar matplotlib o tkinter.Canvas más adelante)
    placeholder = tb.Label(frame, text="[GRÁFICO]", font=("Consolas", 20), bootstyle="secondary")
    placeholder.pack(pady=20)
