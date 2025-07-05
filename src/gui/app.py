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
        self.ventana.geometry("950x750")
        self.ventana.minsize(850, 650)
        
        # Configurar ícono (opcional)
        try:
            # Si tienes un ícono, descomenta esta línea
            # self.ventana.iconbitmap("assets/icon.ico")
            pass
        except:
            pass
        
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
        print("✅ Interfaz gráfica iniciada correctamente")
        print("💡 Tip: Comienza cargando un ejemplo desde la pestaña 'Entrada'")
        print("📁 Ejemplos disponibles en la carpeta 'ejemplos/'")
        print()
        
        # Ejecutar el loop principal
        self.ventana.mainloop()
        
        print("👋 Aplicación cerrada. ¡Gracias por usar el analizador!")

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
