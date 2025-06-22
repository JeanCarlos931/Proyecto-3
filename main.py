#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Principal - Decodificador Gráfico de Mensajes Huffman

Este archivo contiene la interfaz gráfica y coordina los módulos de codificación
y decodificación de Huffman.
"""

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

# Importaciones de módulos propios
from huffman_codificador import (
    codificar_mensaje, 
    analizar_compresion, 
    obtener_estadisticas_codificacion
)
from huffman_decodificador import (
    decodificar_archivo, 
    validar_archivo, 
    analizar_archivo
)

# --------------------------------------------------
# Visualización gráfica (GUI con Tkinter)
# --------------------------------------------------
class VisualizadorHuffman:
    def __init__(self, raiz, bits=""):
        self.raiz = raiz
        self.bits = bits
        self.ventana = tk.Tk()
        self.ventana.title("Decodificador Gráfico de Huffman")
        self.ventana.geometry("1400x800")
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame superior para controles
        frame_controles = tk.Frame(frame_principal)
        frame_controles.pack(fill=tk.X, pady=(0, 20))
        
        # Botones de control
        self.boton_iniciar = tk.Button(
            frame_controles, 
            text="▶ Iniciar Animación", 
            command=self.iniciar_animacion,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15
        )
        self.boton_iniciar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.boton_pausar = tk.Button(
            frame_controles, 
            text="⏸ Pausar", 
            command=self.pausar_animacion,
            bg='#FF9800',
            fg='white',
            font=("Arial", 12),
            width=10,
            state=tk.DISABLED
        )
        self.boton_pausar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.boton_reiniciar = tk.Button(
            frame_controles, 
            text="🔄 Reiniciar", 
            command=self.reiniciar_animacion,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12),
            width=10
        )
        self.boton_reiniciar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.boton_limpiar = tk.Button(
            frame_controles, 
            text="🗑 Limpiar", 
            command=self.limpiar_visualizacion,
            bg='#F44336',
            fg='white',
            font=("Arial", 12),
            width=10
        )
        self.boton_limpiar.pack(side=tk.LEFT)
        
        # Frame para el canvas
        frame_canvas = tk.Frame(frame_principal)
        frame_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para dibujar el árbol
        self.canvas = tk.Canvas(frame_canvas, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior para información
        frame_info = tk.Frame(frame_principal)
        frame_info.pack(fill=tk.X, pady=(20, 0))
        
        # Etiqueta para el mensaje decodificado
        self.etiqueta_mensaje = tk.Label(
            frame_info, 
            text="Mensaje decodificado: ", 
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.etiqueta_mensaje.pack(fill=tk.X)
        
        # Etiqueta para información adicional
        self.etiqueta_info = tk.Label(
            frame_info,
            text="",
            font=("Arial", 10),
            fg='#666'
        )
        self.etiqueta_info.pack(fill=tk.X, pady=(5, 0))
        
        # Variables de control de animación
        self.animacion_activa = False
        self.bit_index = 0
        self.mensaje_decodificado = ""
        self.nodo_actual = raiz
        self.posiciones = {}
        self.nodos_visitados = []  # Lista para rastrear nodos visitados en el recorrido actual
        
        # Dibujar árbol inicial
        self.dibujar_arbol()
        
        # Configurar eventos del canvas
        self.canvas.bind('<Configure>', self.redimensionar_arbol)
        
        self.ventana.mainloop()

    def dibujar_arbol(self):
        """Dibuja el árbol de Huffman en el canvas."""
        self.canvas.delete("all")
        self.posiciones = {}
        
        if self.raiz is None:
            return
        
        # Obtener dimensiones del canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        # Calcular posición inicial
        x_inicial = canvas_width // 2
        y_inicial = 50
        separacion_inicial = min(canvas_width // 4, 300)
        
        self._dibujar_nodo(self.raiz, x_inicial, y_inicial, separacion_inicial)

    def _dibujar_nodo(self, nodo, x, y, separacion):
        """Dibuja recursivamente un nodo y sus hijos."""
        if nodo is None:
            return
        
        self.posiciones[nodo] = (x, y)
        radio = 25
        
        # Color del nodo
        if nodo.caracter is None:
            color = '#E3F2FD'  # Azul claro para nodos internos
        else:
            color = '#C8E6C9'  # Verde claro para hojas
        
        # Dibujar nodo
        self.canvas.create_oval(
            x - radio, y - radio, 
            x + radio, y + radio, 
            fill=color, outline='#1976D2', width=2,
            tags=f"nodo_{id(nodo)}"
        )
        
        # Etiqueta del nodo
        if nodo.caracter is not None:
            texto = f"'{nodo.caracter}'\n{nodo.frecuencia}"
        else:
            texto = f"{nodo.frecuencia}"
        
        self.canvas.create_text(
            x, y, text=texto, font=("Arial", 10, "bold"),
            tags=f"texto_{id(nodo)}"
        )
        
        # Conexiones a hijos
        nueva_separacion = separacion * 0.6
        nueva_y = y + 100
        
        if nodo.izquierda:
            x_izq = x - separacion
            # Línea a hijo izquierdo
            self.canvas.create_line(
                x, y + radio, 
                x_izq, nueva_y - radio, 
                arrow=tk.LAST, fill='#1976D2', width=2
            )
            # Etiqueta "0"
            self.canvas.create_text(
                (x + x_izq) // 2, (y + nueva_y) // 2,
                text="0", font=("Arial", 12, "bold"),
                fill='#1976D2'
            )
            self._dibujar_nodo(nodo.izquierda, x_izq, nueva_y, nueva_separacion)
        
        if nodo.derecha:
            x_der = x + separacion
            # Línea a hijo derecho
            self.canvas.create_line(
                x, y + radio, 
                x_der, nueva_y - radio, 
                arrow=tk.LAST, fill='#1976D2', width=2
            )
            # Etiqueta "1"
            self.canvas.create_text(
                (x + x_der) // 2, (y + nueva_y) // 2,
                text="1", font=("Arial", 12, "bold"),
                fill='#1976D2'
            )
            self._dibujar_nodo(nodo.derecha, x_der, nueva_y, nueva_separacion)

    def redimensionar_arbol(self, event=None):
        """Redimensiona el árbol cuando cambia el tamaño del canvas."""
        self.dibujar_arbol()

    def limpiar_colores_recorrido(self):
        """Limpia los colores de todos los nodos visitados en el recorrido actual."""
        for nodo in self.nodos_visitados:
            self.restaurar_color_nodo(nodo)
        self.nodos_visitados.clear()

    def restaurar_color_nodo(self, nodo):
        """Restaura el color original de un nodo."""
        if nodo in self.posiciones:
            x, y = self.posiciones[nodo]
            radio = 25
            
            # Color original del nodo
            if nodo.caracter is None:
                color = '#E3F2FD'  # Azul claro para nodos internos
            else:
                color = '#C8E6C9'  # Verde claro para hojas
            
            # Actualizar color del nodo
            self.canvas.delete(f"nodo_{id(nodo)}")
            self.canvas.create_oval(
                x - radio, y - radio, 
                x + radio, y + radio, 
                fill=color, outline='#1976D2', width=2,
                tags=f"nodo_{id(nodo)}"
            )
            
            # Redibujar texto
            self.canvas.delete(f"texto_{id(nodo)}")
            if nodo.caracter is not None:
                texto = f"'{nodo.caracter}'\n{nodo.frecuencia}"
            else:
                texto = f"{nodo.frecuencia}"
            
            self.canvas.create_text(
                x, y, text=texto, font=("Arial", 10, "bold"),
                tags=f"texto_{id(nodo)}"
            )

    def iniciar_animacion(self):
        """Inicia la animación de decodificación paso a paso."""
        if not self.bits:
            messagebox.showwarning("Advertencia", "No hay bits para decodificar")
            return
        
        self.animacion_activa = True
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_pausar.config(state=tk.NORMAL)
        self.animar_paso()

    def pausar_animacion(self):
        """Pausa la animación."""
        self.animacion_activa = False
        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_pausar.config(state=tk.DISABLED)

    def reiniciar_animacion(self):
        """Reinicia la animación desde el principio."""
        self.animacion_activa = False
        self.bit_index = 0
        self.mensaje_decodificado = ""
        self.nodo_actual = self.raiz
        self.nodos_visitados.clear()
        self.etiqueta_mensaje.config(text="Mensaje decodificado: ")
        self.etiqueta_info.config(text="")
        
        # Restaurar colores originales
        self.dibujar_arbol()
        
        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_pausar.config(state=tk.DISABLED)

    def limpiar_visualizacion(self):
        """Limpia la visualización y cierra la ventana."""
        self.ventana.destroy()

    def animar_paso(self):
        """Ejecuta un paso de la animación."""
        if not self.animacion_activa or self.bit_index >= len(self.bits):
            self.animacion_activa = False
            self.boton_iniciar.config(state=tk.NORMAL)
            self.boton_pausar.config(state=tk.DISABLED)
            return
        
        bit = self.bits[self.bit_index]
        self.bit_index += 1
        
        # Actualizar información
        self.etiqueta_info.config(
            text=f"Bit {self.bit_index}/{len(self.bits)}: {bit} | "
                 f"Caracteres decodificados: {len(self.mensaje_decodificado)}"
        )
        
        # Actualizar nodo actual
        if bit == '0':
            self.nodo_actual = self.nodo_actual.izquierda
        else:
            self.nodo_actual = self.nodo_actual.derecha
        
        # Agregar nodo actual a la lista de visitados
        self.nodos_visitados.append(self.nodo_actual)
        
        # Resaltar nodo actual
        self.resaltar_nodo(self.nodo_actual, '#FFEB3B')  # Amarillo
        
        # Verificar si es hoja
        if self.nodo_actual.caracter is not None:
            self.mensaje_decodificado += self.nodo_actual.caracter
            self.etiqueta_mensaje.config(
                text=f"Mensaje decodificado: {self.mensaje_decodificado}"
            )
            # Resaltar hoja encontrada
            self.resaltar_nodo(self.nodo_actual, '#4CAF50')  # Verde
            
            # Limpiar colores del recorrido anterior
            self.limpiar_colores_recorrido()
            
            # Reiniciar para el siguiente carácter
            self.nodo_actual = self.raiz
        
        # Programar siguiente paso
        if self.animacion_activa:
            self.ventana.after(500, self.animar_paso)

    def resaltar_nodo(self, nodo, color):
        """Resalta un nodo con el color especificado."""
        if nodo in self.posiciones:
            x, y = self.posiciones[nodo]
            radio = 25
            
            # Actualizar color del nodo
            self.canvas.delete(f"nodo_{id(nodo)}")
            self.canvas.create_oval(
                x - radio, y - radio, 
                x + radio, y + radio, 
                fill=color, outline='#1976D2', width=2,
                tags=f"nodo_{id(nodo)}"
            )
            
            # Redibujar texto
            self.canvas.delete(f"texto_{id(nodo)}")
            if nodo.caracter is not None:
                texto = f"'{nodo.caracter}'\n{nodo.frecuencia}"
            else:
                texto = f"{nodo.frecuencia}"
            
            self.canvas.create_text(
                x, y, text=texto, font=("Arial", 10, "bold"),
                tags=f"texto_{id(nodo)}"
            )

# --------------------------------------------------
# Interfaz principal
# --------------------------------------------------
class InterfazPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("The Turing's Forest")
        self.ventana.geometry("700x500")
        self.ventana.configure(bg='#f5f5f5')
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg='#f5f5f5')
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Título
        titulo = tk.Label(
            frame_principal, 
            text="🌳🌳🌳 The Turing's Forest 🌳🌳🌳", 
            font=("Arial", 24, "bold"),
            bg='#f5f5f5',
            fg="#1DD401"
        )
        titulo.pack(pady=(0, 40))
        
        # Frame para botones
        frame_botones = tk.Frame(frame_principal, bg='#f5f5f5')
        frame_botones.pack()
        
        # Botón para codificar
        boton_codificar = tk.Button(
            frame_botones, 
            text="Codificar Mensaje", 
            command=self.codificar_mensaje,
            width=25, height=3,
            font=("Arial", 14, "bold"),
            bg='#4CAF50',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2'
        )
        boton_codificar.pack(pady=15)
        
        # Botón para decodificar
        boton_decodificar = tk.Button(
            frame_botones, 
            text="Decodificar Archivo", 
            command=self.decodificar_archivo,
            width=25, height=3,
            font=("Arial", 14, "bold"),
            bg='#2196F3',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2'
        )
        boton_decodificar.pack(pady=15)
        
        # Botón para salir
        boton_salir = tk.Button(
            frame_botones, 
            text="Salir", 
            command=self.ventana.quit,
            width=25, height=2,
            font=("Arial", 12),
            bg='#F44336',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2'
        )
        boton_salir.pack(pady=15)
        
        self.ventana.mainloop()
    
    def codificar_mensaje(self):
        """Permite al usuario codificar un mensaje."""
        mensaje = simpledialog.askstring(
            "Codificar Mensaje", 
            "Ingrese el mensaje a codificar:",
            parent=self.ventana
        )
        
        if mensaje:
            if not mensaje.strip():
                messagebox.showwarning("Advertencia", "El mensaje no puede estar vacío")
                return
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".bin",
                filetypes=[("Archivos binarios", "*.bin"), ("Todos los archivos", "*.*")],
                title="Guardar archivo codificado"
            )
            
            if archivo:
                try:
                    # Usar función del módulo de codificación
                    stats, raiz, codigos, bits = obtener_estadisticas_codificacion(mensaje, archivo)
                    
                    # Mostrar información de la codificación
                    info_text = f"Mensaje codificado exitosamente!\n\n"
                    info_text += f"Archivo guardado: {os.path.basename(archivo)}\n"
                    info_text += f"Tamaño original: {stats['tamaño_original_bytes']} bytes\n"
                    info_text += f"Tamaño comprimido: {stats['tamaño_comprimido_bytes']} bytes\n"
                    info_text += f"Compresión: {stats['compresion_porcentaje']:.1f}%\n\n"
                    info_text += "Códigos generados:\n"
                    
                    for caracter, codigo in sorted(codigos.items()):
                        info_text += f"'{caracter}': {codigo}\n"
                    
                    messagebox.showinfo("Codificación Exitosa", info_text)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al codificar el mensaje: {str(e)}")
    
    def decodificar_archivo(self):
        """Permite al usuario decodificar un archivo."""
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos binarios", "*.bin"), ("Todos los archivos", "*.*")],
            title="Seleccionar archivo para decodificar"
        )
        
        if archivo:
            try:
                # Validar archivo primero
                validacion = validar_archivo(archivo)
                if not validacion['valido']:
                    messagebox.showerror("Error", f"Archivo inválido: {validacion['error']}")
                    return
                
                # Usar función del módulo de decodificación
                mensaje, raiz, bits = decodificar_archivo(archivo)
                
                # Mostrar mensaje decodificado
                messagebox.showinfo(
                    "Decodificación Exitosa", 
                    f"Archivo decodificado exitosamente!\n\n"
                    f"Mensaje: {mensaje}\n"
                    f"Longitud: {len(mensaje)} caracteres\n"
                    f"Bits procesados: {len(bits)}"
                )
                
                # Abrir visualizador
                VisualizadorHuffman(raiz, bits)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al decodificar el archivo: {str(e)}")

# --------------------------------------------------
# Función principal
# --------------------------------------------------
if __name__ == "__main__":
    try:
        InterfazPrincipal()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")