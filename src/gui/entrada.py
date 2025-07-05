import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import ttkbootstrap as tb
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pseudogrammar import tokenizar
from core.parser_estructural import parsear
from core.analizador_complejidad import AnalizadorComplejidad
from core.serializacion import SerializadorAnalisis

def crear_pestana_entrada(frame, cambiar_a_grafica_callback=None, cambiar_a_comparacion_callback=None):
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

    def limpiar_texto():
        texto_codigo.delete(1.0, "end")
        texto_resultado.config(state="normal")
        texto_resultado.delete(1.0, "end")
        texto_resultado.config(state="disabled")
        nonlocal ultimo_resultado
        ultimo_resultado = None

    def analizar_codigo():
        codigo = texto_codigo.get(1.0, "end-1c").strip()
        if not codigo:
            tkinter.messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
            return
        
        try:
            # Tokenizar y parsear
            tokens = tokenizar(codigo)
            arbol = parsear(tokens)
            
            # Buscar funciones en el árbol
            funciones = encontrar_funciones(arbol)
            
            if funciones:
                # Si hay funciones, analizar la primera
                nombre_funcion = funciones[0]
                analizador = AnalizadorComplejidad(arbol)
                resultado = analizador.analizar(nombre_funcion)
            else:
                # Si no hay funciones definidas, analizar el programa completo
                analizador = AnalizadorComplejidad(arbol)
                resultado = analizador.analizar()
            
            # Mostrar resultado
            texto_resultado.config(state="normal")
            texto_resultado.delete(1.0, "end")
            
            resultado_texto = "✅ ANÁLISIS COMPLETADO EXITOSAMENTE\n"
            resultado_texto += "═" * 45 + "\n\n"
            
            if resultado.nombre_funcion:
                resultado_texto += f"🔧 Función: {resultado.nombre_funcion}\n"
            else:
                resultado_texto += f"🔧 Código: Programa principal\n"
                
            if resultado.recursivo:
                resultado_texto += "🔄 Tipo: Función recursiva\n"
            else:
                resultado_texto += "➡️  Tipo: Función iterativa\n"
                
            resultado_texto += f"⏱️  T(n) = {resultado.funcion_tiempo.como_str()}\n"
            resultado_texto += f"📈 Big O: {resultado.big_o}\n\n"
            
            # Interpretación del resultado
            resultado_texto += "📊 INTERPRETACIÓN:\n"
            resultado_texto += "─" * 20 + "\n"
            
            if "O(1)" in resultado.big_o:
                resultado_texto += "🟢 Complejidad constante - Muy eficiente\n"
            elif "log" in resultado.big_o.lower():
                resultado_texto += "🟢 Complejidad logarítmica - Muy eficiente\n"
            elif "O(n)" == resultado.big_o:
                resultado_texto += "🟡 Complejidad lineal - Eficiencia buena\n"
            elif "n**2" in resultado.big_o or "n^2" in resultado.big_o:
                resultado_texto += "🟠 Complejidad cuadrática - Cuidado con datos grandes\n"
            elif "2**n" in resultado.big_o or "2^n" in resultado.big_o:
                resultado_texto += "🔴 Complejidad exponencial - Solo para datos pequeños\n"
            else:
                resultado_texto += "⚪ Complejidad personalizada - Analiza caso por caso\n"
            
            resultado_texto += "\n💡 Usa las pestañas 'Gráfica' y 'Comparación' para más detalles"
            
            texto_resultado.insert("end", resultado_texto)
            texto_resultado.config(state="disabled")
            
            # Guardar resultado para uso posterior
            nonlocal ultimo_resultado
            ultimo_resultado = resultado
            
            # Habilitar botones después del análisis exitoso
            boton_ver_grafica.config(state="normal")
            boton_guardar.config(state="normal")
            boton_comparar.config(state="normal")
            
        except Exception as e:
            texto_resultado.config(state="normal")
            texto_resultado.delete(1.0, "end")
            
            error_msg = f"❌ Error en el análisis:\n\n"
            error_msg += f"📋 Detalles: {str(e)}\n\n"
            error_msg += "🔧 Posibles soluciones:\n"
            error_msg += "• Verifica que el código siga la sintaxis correcta\n"
            error_msg += "• Asegúrate de que las funciones estén bien definidas\n"
            error_msg += "• Revisa que los bucles tengan condiciones de parada\n"
            error_msg += "• Consulta los ejemplos en la carpeta 'ejemplos/'\n\n"
            error_msg += "💡 Sintaxis básica:\n"
            error_msg += "Funcion nombreFuncion(N)\n"
            error_msg += "    // tu código aquí\n"
            error_msg += "fFuncion"
            
            texto_resultado.insert("end", error_msg)
            texto_resultado.config(state="disabled")
            
            # Deshabilitar botones si hay error
            boton_ver_grafica.config(state="disabled")
            boton_guardar.config(state="disabled")
            boton_comparar.config(state="disabled")

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

    def guardar_analisis():
        if ultimo_resultado is None:
            tkinter.messagebox.showwarning("Advertencia", "No hay análisis para guardar. Primero analice el código.")
            return
        
        codigo = texto_codigo.get(1.0, "end-1c")
        nombre = tkinter.simpledialog.askstring("Guardar análisis", "Nombre para el archivo:")
        
        if nombre:
            try:
                ruta = serializador.guardar_analisis(codigo, ultimo_resultado, nombre)
                tkinter.messagebox.showinfo("Éxito", f"Análisis guardado en:\n{ruta}")
            except Exception as e:
                tkinter.messagebox.showerror("Error", f"No se pudo guardar el análisis:\n{str(e)}")

    def ver_grafica():
        if ultimo_resultado is None:
            tkinter.messagebox.showwarning("Advertencia", "No hay análisis para graficar. Primero analice el código.")
            return
        
        if cambiar_a_grafica_callback:
            # Pasar el resultado al callback para que la pestaña de gráfica lo use
            cambiar_a_grafica_callback(ultimo_resultado)

    def comparar_algoritmo():
        if ultimo_resultado is None:
            tkinter.messagebox.showwarning("Advertencia", "No hay análisis para comparar. Primero analice el código.")
            return
        
        if cambiar_a_comparacion_callback:
            codigo = texto_codigo.get(1.0, "end-1c")
            cambiar_a_comparacion_callback(ultimo_resultado, codigo)

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
    boton_cargar.pack(side="left", padx=5)

    boton_analizar = tb.Button(frame_botones, text="Analizar", command=analizar_codigo, bootstyle="info")
    boton_analizar.pack(side="left", padx=5)

    boton_guardar = tb.Button(frame_botones, text="Guardar", command=guardar_analisis, bootstyle="warning", state="disabled")
    boton_guardar.pack(side="left", padx=5)

    # --- RESULTADO DEL ANÁLISIS ---
    etiqueta_resultado = tb.Label(frame, text="Resultado del análisis:", font=("Segoe UI", 11, "bold"))
    etiqueta_resultado.pack(anchor="w", padx=20, pady=(15, 5))

    texto_resultado = tb.Text(frame, wrap="word", font=("Segoe UI", 11), height=8, state="disabled")
    texto_resultado.pack(fill="both", expand=False, padx=20, pady=(0, 10))

    # --- BOTONES INFERIORES ---
    frame_inferior = tb.Frame(frame)
    frame_inferior.pack(pady=10)

    boton_ver_grafica = tb.Button(frame_inferior, text="Ver gráfica", bootstyle="primary", command=ver_grafica, state="disabled")
    boton_ver_grafica.pack(side="left", padx=10)

    boton_comparar = tb.Button(frame_inferior, text="Comparar algoritmo", bootstyle="secondary", command=comparar_algoritmo, state="disabled")
    boton_comparar.pack(side="left", padx=10)