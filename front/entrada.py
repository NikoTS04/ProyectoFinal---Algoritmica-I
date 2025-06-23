import tkinter.filedialog
import ttkbootstrap as tb

def crear_pestana_entrada(frame, cambiar_a_grafica_callback=None):
    # --- FUNCIONES ---
    def cargar_archivo():
        archivo = tkinter.filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            with open(archivo, 'r') as f:
                contenido = f.read()
                texto_codigo.delete(1.0, "end")
                texto_codigo.insert("end", contenido)

    def limpiar_texto():
        texto_codigo.delete(1.0, "end")

    def ver_grafica():
        if cambiar_a_grafica_callback:
            cambiar_a_grafica_callback()

    # --- ETIQUETA Y LIMPIAR ---
    encabezado = tb.Frame(frame)
    encabezado.pack(fill="x", padx=20, pady=(15, 5))

    etiqueta_codigo = tb.Label(encabezado, text="Ingrese su código aquí:", font=("Segoe UI", 11, "bold"))
    etiqueta_codigo.pack(side="left")

    boton_limpiar = tb.Button(encabezado, text="Limpiar", command=limpiar_texto, bootstyle="warning-outline")
    boton_limpiar.pack(side="right")

    # --- CAJA DE TEXTO DE ENTRADA ---
    texto_codigo = tb.Text(frame, wrap="word", font=("Segoe UI", 11), height=12)
    texto_codigo.pack(fill="both", expand=False, padx=20, pady=(0, 10))

    scroll = tb.Scrollbar(frame, command=texto_codigo.yview)
    scroll.place(in_=texto_codigo, relx=1.0, rely=0, relheight=1.0, anchor="ne")
    texto_codigo.config(yscrollcommand=scroll.set)

    # --- BOTONES DE ACCIÓN ---
    frame_botones = tb.Frame(frame)
    frame_botones.pack(pady=10)

    boton_cargar = tb.Button(frame_botones, text="Cargar archivo", command=cargar_archivo, bootstyle="success")
    boton_cargar.pack(side="left", padx=10)

    boton_analizar = tb.Button(frame_botones, text="Analizar", command=lambda: print("Análisis pendiente..."), bootstyle="info")
    boton_analizar.pack(side="left", padx=10)

    # --- RESULTADO DEL ANÁLISIS ---
    etiqueta_resultado = tb.Label(frame, text="Resultado del análisis:", font=("Segoe UI", 11, "bold"))
    etiqueta_resultado.pack(anchor="w", padx=20, pady=(15, 5))

    texto_resultado = tb.Text(frame, wrap="word", font=("Segoe UI", 11), height=8, state="normal")
    texto_resultado.pack(fill="both", expand=False, padx=20, pady=(0, 10))

    # --- BOTONES INFERIORES ---
    frame_inferior = tb.Frame(frame)
    frame_inferior.pack(pady=10)

    boton_ver_grafica = tb.Button(frame_inferior, text="Ver gráfica", bootstyle="primary", command=ver_grafica)
    boton_ver_grafica.pack(side="left", padx=10)

    boton_comparar = tb.Button(frame_inferior, text="Comparar con otro algoritmo", bootstyle="secondary")
    boton_comparar.pack(side="left", padx=10)