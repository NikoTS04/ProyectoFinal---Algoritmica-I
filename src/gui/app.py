#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Principal de la GUI
=============================

Punto de entrada para la interfaz gráfica del analizador de complejidad temporal.
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Importar módulos de la GUI
from gui.entrada import crear_pestana_entrada
from gui.grafica import crear_pestana_grafica
from gui.comparacion import crear_pestana_comparacion

class AnalizadorApp:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        # Configurar matplotlib para usar backend compatible con tkinter
        import matplotlib
        matplotlib.use('TkAgg')
        
        # Crear ventana principal
        self.ventana = tb.Window(themename="flatly")
        self.ventana.title("🎯 Analizador de Complejidad Temporal - v2.0")
        self.ventana.geometry("1000x800")
        self.ventana.minsize(900, 700)
        
        # Maximizar ventana si es Windows
        try:
            self.ventana.state('zoomed')
        except:
            # Si no es Windows, usar normal
            pass
        
        # Configurar ícono personalizado
        self._configurar_icono()
        
        # Configurar ventana para Windows (barra de tareas)
        self._configurar_ventana_windows()
        
        # Crear el Notebook (pestañas)
        self.notebook = tb.Notebook(self.ventana, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear frames para cada pestaña
        self.frame_entrada = tb.Frame(self.notebook)
        self.frame_grafica = tb.Frame(self.notebook)
        self.frame_comparacion = tb.Frame(self.notebook)
        
        # Variables globales para comunicación entre pestañas
        self.resultado_actual = None
        
        # Configurar pestañas
        self._configurar_pestanas()
        
        # Añadir las pestañas al notebook
        self.notebook.add(self.frame_entrada, text=" 📝 Entrada ")
        self.notebook.add(self.frame_grafica, text=" 📊 Gráfica ")
        self.notebook.add(self.frame_comparacion, text=" ⚖️ Comparación ")
        
        # Barra de estado
        self.frame_status = tb.Frame(self.ventana)
        self.frame_status.pack(fill="x", padx=10, pady=(0, 5))
        
        self.label_status = tb.Label(
            self.frame_status, 
            text="🚀 Listo para analizar | 💡 Tip: Carga un ejemplo desde 'Entrada'",
            bootstyle="info",
            font=("Segoe UI", 9)
        )
        self.label_status.pack(side="left", padx=5)
        
        # Información de versión
        self.label_version = tb.Label(
            self.frame_status,
            text="v2.0",
            bootstyle="secondary",
            font=("Segoe UI", 8)
        )
        self.label_version.pack(side="right", padx=5)
        
        # Configurar eventos de cierre
        self.ventana.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _configurar_icono(self):
        """Configura el icono personalizado de la aplicación"""
        try:
            # Ruta al icono desde la ubicación del archivo app.py
            icon_path = Path(__file__).parent.parent / "resources" / "gatoCoder.ico"
            
            if icon_path.exists():
                # Método 1: iconbitmap (ventana principal)
                self.ventana.iconbitmap(str(icon_path))
                
                # Método 2: wm_iconbitmap (compatibilidad adicional)
                self.ventana.wm_iconbitmap(str(icon_path))
                
                # Método 3: iconphoto para mayor compatibilidad con sistemas modernos
                try:
                    from PIL import Image, ImageTk
                    # Cargar el icono
                    image = Image.open(icon_path)
                    # Convertir a RGBA si es necesario
                    if image.mode != 'RGBA':
                        image = image.convert('RGBA')
                    # Crear PhotoImage
                    photo = ImageTk.PhotoImage(image)
                    # Aplicar a todas las ventanas (True = aplicar globalmente)
                    self.ventana.iconphoto(True, photo)
                    # Mantener una referencia para evitar que sea recolectado por garbage collector
                    self.ventana._icon_photo = photo
                    
                except ImportError:
                    print("⚠️ PIL no disponible, usando solo iconbitmap")
                except Exception as e:
                    print(f"⚠️ Error con iconphoto: {e}")
                
                print(f" Icono personalizado cargado: {icon_path.name}")
                print(" Icono aplicado a ventana y barra de tareas")
                
            else:
                print(f" Archivo de icono no encontrado: {icon_path}")
                print(f" Buscado en: {icon_path}")
                
                # Buscar en ubicaciones alternativas
                alt_paths = [
                    Path(__file__).parent.parent.parent / "resources" / "gatoCoder.ico",
                    Path(__file__).parent / "resources" / "gatoCoder.ico", 
                    Path("resources") / "gatoCoder.ico",
                    Path("gatoCoder.ico")
                ]
                
                for alt_path in alt_paths:
                    if alt_path.exists():
                        print(f" Icono encontrado en ubicación alternativa: {alt_path}")
                        self.ventana.iconbitmap(str(alt_path))
                        self.ventana.wm_iconbitmap(str(alt_path))
                        break
                else:
                    print(" No se encontró el icono en ninguna ubicación")
                    
        except Exception as e:
            print(f"⚠️ No se pudo cargar el icono personalizado: {e}")
            print("💡 La aplicación usará el icono por defecto")
    
    def _configurar_ventana_windows(self):
        """Configuraciones específicas para Windows (barra de tareas)"""
        try:
            # Configurar ID único de aplicación para Windows
            import ctypes
            app_id = 'UCSUR.AnalizadorComplejidad.GUI.2.0'  # ID único para tu app
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
            # Configurar atributos adicionales de la ventana
            self.ventana.attributes('-toolwindow', False)  # Asegurar que aparezca en barra de tareas
            
            # Forzar que la ventana sea reconocida como aplicación independiente
            self.ventana.wm_attributes('-topmost', False)
            
            print(" Configuraciones de Windows aplicadas (barra de tareas)")
            
        except Exception as e:
            print(f" No se pudieron aplicar configuraciones de Windows: {e}")
            # No es crítico, continuar sin estas optimizaciones
            pass
    
    def _configurar_pestanas(self):
        """Configura el contenido de cada pestaña"""
        
        # Crear contenido de las pestañas con callbacks
        crear_pestana_entrada(
            self.frame_entrada, 
            self._cambiar_a_grafica, 
            self._cambiar_a_comparacion
        )
        
        crear_pestana_grafica(self.frame_grafica)
        
        crear_pestana_comparacion(self.frame_comparacion)
    
    def _cambiar_a_grafica(self, resultado_analisis=None):
        """Cambia a la pestaña de gráfica y actualiza con resultado"""
        if resultado_analisis:
            self.resultado_actual = resultado_analisis
            # Actualizar gráfica si la función existe
            if hasattr(self.frame_grafica, 'actualizar_grafica'):
                self.frame_grafica.actualizar_grafica(resultado_analisis)
        self.notebook.select(self.frame_grafica)
    
    def _cambiar_a_comparacion(self, resultado_analisis=None, codigo=""):
        """Cambia a la pestaña de comparación"""
        if resultado_analisis and hasattr(self.frame_comparacion, 'establecer_algoritmo1'):
            self.frame_comparacion.establecer_algoritmo1(resultado_analisis, codigo)
        self.notebook.select(self.frame_comparacion)
    
    def _on_closing(self):
        """Maneja el evento de cierre de la aplicación"""
        try:
            # Cerrar todas las figuras de matplotlib
            import matplotlib.pyplot as plt
            plt.close('all')
        except:
            pass
        
        # Cerrar la ventana
        self.ventana.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        print(" Interfaz gráfica iniciada correctamente")
        print(" Tip: Comienza cargando un ejemplo desde la pestaña 'Entrada'")
        print(" Ejemplos disponibles en la carpeta 'ejemplos/'")
        print()
        
        # Ejecutar el loop principal
        self.ventana.mainloop()
        
        print(" Aplicación cerrada.")

def main():
    """Función principal para ejecutar la aplicación"""
    try:
        app = AnalizadorApp()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
