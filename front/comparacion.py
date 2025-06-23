import ttkbootstrap as tb

def crear_pestana_comparacion(frame):
    etiqueta = tb.Label(frame, text="Comparación de resultados entre algoritmos.", font=("Segoe UI", 12))
    etiqueta.pack(padx=10, pady=20)

    # Dummy tabla o texto
    placeholder = tb.Label(frame, text="[TABLA DE COMPARACIÓN]", font=("Consolas", 20), bootstyle="secondary")
    placeholder.pack(pady=20)
