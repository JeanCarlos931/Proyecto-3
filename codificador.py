#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Codificación Huffman

Este módulo contiene todas las funcionalidades relacionadas con la codificación
de mensajes usando el algoritmo de Huffman.
"""

import heapq
import struct
import os
from collections import defaultdict

# --------------------------------------------------
# Estructuras de Datos
# --------------------------------------------------
class NodoArbol:
    
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro):
        """Permite comparar nodos por frecuencia para el heap."""
        return self.frecuencia < otro.frecuencia

# --------------------------------------------------
# Funciones de Análisis
# --------------------------------------------------
def calcular_frecuencias(mensaje):
    """
    Calcula la frecuencia de cada carácter en el mensaje.
    
    Args:
        mensaje (str): El mensaje a analizar
        
    Returns:
        defaultdict: Diccionario con caracteres como claves y frecuencias como valores
    """
    frecuencias = defaultdict(int)
    for caracter in mensaje:
        frecuencias[caracter] += 1
    return frecuencias

# --------------------------------------------------
# Construcción del Árbol
# --------------------------------------------------
def construir_arbol(frecuencias):
    """
    Construye el árbol de Huffman a partir de las frecuencias.
    
    Args:
        frecuencias (dict): Diccionario de frecuencias de caracteres
        
    Returns:
        NodoHuffman: Raíz del árbol construido, o None si no hay frecuencias
    """
    if not frecuencias:
        return None
    
    # Crear nodos iniciales
    monticulo = [NodoArbol(caracter, freq) for caracter, freq in frecuencias.items()]
    heapq.heapify(monticulo)
    
    # Construir árbol combinando nodos
    while len(monticulo) > 1:
        izquierda = heapq.heappop(monticulo)
        derecha = heapq.heappop(monticulo)
        
        # Crear nodo padre
        nodo_padre = NodoArbol(None, izquierda.frecuencia + derecha.frecuencia)
        nodo_padre.izquierda = izquierda
        nodo_padre.derecha = derecha
        
        heapq.heappush(monticulo, nodo_padre)
    
    return monticulo[0] if monticulo else None

# --------------------------------------------------
# Generación de Códigos
# --------------------------------------------------
def generar_codigos(raiz, codigo_actual="", codigos=None):
    """
    Genera los códigos de Huffman para cada carácter.
    
    Args:
        raiz (NodoHuffman): Raíz del árbol de Huffman
        codigo_actual (str): Código binario actual (para recursión)
        codigos (dict): Diccionario de códigos (para recursión)
        
    Returns:
        dict: Diccionario con caracteres como claves y códigos binarios como valores
    """
    if codigos is None:
        codigos = {}
    
    if raiz is None:
        return {}
    
    # Si es una hoja, guardar el código
    if raiz.caracter is not None:
        codigos[raiz.caracter] = codigo_actual
        return codigos
    
    # Recursión para hijos izquierdo (0) y derecho (1)
    generar_codigos(raiz.izquierda, codigo_actual + "0", codigos)
    generar_codigos(raiz.derecha, codigo_actual + "1", codigos)
    
    return codigos

# --------------------------------------------------
# Codificación de Mensaje
# --------------------------------------------------
def codificar_mensaje(mensaje, nombre_archivo):
    """
    Codifica un mensaje y lo guarda en un archivo .bin.
    
    Args:
        mensaje (str): El mensaje a codificar
        nombre_archivo (str): Ruta del archivo donde guardar
        
    Returns:
        tuple: (raiz_arbol, codigos, bits_codificados)
        
    Raises:
        ValueError: Si el mensaje está vacío
        IOError: Si hay problemas al escribir el archivo
    """
    if not mensaje:
        raise ValueError("El mensaje no puede estar vacío")
    
    # Paso 1: Calcular frecuencias
    frecuencias = calcular_frecuencias(mensaje)
    
    # Paso 2: Construir árbol
    raiz = construir_arbol(frecuencias)
    
    # Paso 3: Generar códigos
    codigos = generar_codigos(raiz)
    
    # Paso 4: Codificar mensaje
    bits = ''.join(codigos[caracter] for caracter in mensaje)
    
    # Paso 5: Guardar en archivo
    with open(nombre_archivo, 'wb') as archivo:
        # Escribir cantidad de caracteres únicos (4 bytes)
        archivo.write(struct.pack('>I', len(frecuencias)))
        
        # Escribir caracteres y frecuencias (3 bytes cada uno)
        for caracter, freq in frecuencias.items():
            archivo.write(struct.pack('>cH', caracter.encode('utf-8'), freq))
        
        # Calcular y escribir bits de relleno
        bits_restantes = len(bits) % 8
        bits_descartados = (8 - bits_restantes) % 8
        archivo.write(struct.pack('>B', bits_descartados))
        
        # Escribir mensaje codificado en bytes
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8].ljust(8, '0')
            archivo.write(bytes([int(byte, 2)]))
    
    return raiz, codigos, bits

# --------------------------------------------------
# Funciones de Análisis y Estadísticas
# --------------------------------------------------
def analizar_compresion(mensaje, codigos):
    """
    Analiza la compresión obtenida con los códigos de Huffman.
    
    Args:
        mensaje (str): Mensaje original
        codigos (dict): Códigos de Huffman generados
        
    Returns:
        dict: Estadísticas de compresión
    """
    bits_original = len(mensaje) * 8  # ASCII
    bits_comprimido = sum(len(codigos[caracter]) for caracter in mensaje)
    bytes_comprimido = (bits_comprimido // 8) + 1
    
    return {
        'tamaño_original_bits': bits_original,
        'tamaño_original_bytes': bits_original // 8,
        'tamaño_comprimido_bits': bits_comprimido,
        'tamaño_comprimido_bytes': bytes_comprimido,
        'compresion_porcentaje': ((1 - bytes_comprimido / (bits_original // 8)) * 100),
        'ratio_compresion': (bits_original // 8) / bytes_comprimido
    }

def obtener_estadisticas_codificacion(mensaje, nombre_archivo):
    """
    Obtiene estadísticas completas de la codificación.
    
    Args:
        mensaje (str): Mensaje original
        nombre_archivo (str): Archivo donde se guardó
        
    Returns:
        dict: Estadísticas completas
    """
    # Realizar codificación
    raiz, codigos, bits = codificar_mensaje(mensaje, nombre_archivo)
    
    # Obtener estadísticas
    stats = analizar_compresion(mensaje, codigos)
    stats['archivo'] = nombre_archivo
    stats['tamaño_archivo'] = os.path.getsize(nombre_archivo)
    stats['caracteres_unicos'] = len(codigos)
    stats['bits_codificados'] = len(bits)
    
    return stats, raiz, codigos, bits

# --------------------------------------------------
# Funciones de Utilidad
# --------------------------------------------------
def mostrar_codigos(codigos):
    """
    Muestra los códigos generados de forma ordenada.
    
    Args:
        codigos (dict): Códigos de Huffman
    """
    print("Códigos de Huffman generados:")
    for caracter, codigo in sorted(codigos.items()):
        print(f"  '{caracter}': {codigo}")

def mostrar_estadisticas(stats):
    """
    Muestra las estadísticas de compresión.
    
    Args:
        stats (dict): Estadísticas de compresión
    """
    print(f"\nEstadísticas de compresión:")
    print(f"  Tamaño original: {stats['tamaño_original_bytes']} bytes")
    print(f"  Tamaño comprimido: {stats['tamaño_comprimido_bytes']} bytes")
    print(f"  Compresión: {stats['compresion_porcentaje']:.1f}%")
    print(f"  Ratio de compresión: {stats['ratio_compresion']:.2f}:1")

# --------------------------------------------------
# Función de Prueba
# --------------------------------------------------
def prueba_codificacion():
    """Función de prueba para verificar el funcionamiento del módulo."""
    mensaje = "HOLA MUNDO"
    archivo_temp = "prueba_codificacion.bin"
    
    try:
        print("=== PRUEBA DE CODIFICACIÓN ===")
        print(f"Mensaje: '{mensaje}'")
        
        # Codificar
        raiz, codigos, bits = codificar_mensaje(mensaje, archivo_temp)
        
        # Mostrar resultados
        mostrar_codigos(codigos)
        stats = analizar_compresion(mensaje, codigos)
        mostrar_estadisticas(stats)
        
        print(f"Archivo guardado: {archivo_temp}")
        
        # Limpiar
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
            
        return True
        
    except Exception as e:
        print(f"Error en prueba: {e}")
        return False

if __name__ == "__main__":
    prueba_codificacion() 