import heapq
import struct
import os
from collections import defaultdict


class NodoArbol:
    """
    Representa un nodo en el árbol de Huffman.
    
    Attributes:
        caracter (str): El carácter almacenado en el nodo (None para nodos internos)
        frecuencia (int): Frecuencia del carácter o suma de frecuencias de hijos
        izquierda (NodoArbol): Hijo izquierdo del nodo
        derecha (NodoArbol): Hijo derecho del nodo
    """
    
    def __init__(self, caracter: str, frecuencia: int) -> None:
        """
        Inicializa un nodo del árbol de Huffman.
        
        Args:
            caracter: El carácter almacenado en el nodo (None para nodos internos)
            frecuencia: Frecuencia del carácter o suma de frecuencias de hijos
        """
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro: 'NodoArbol') -> bool:
        """
        Permite comparar nodos por frecuencia para el heap.
        
        Args:
            otro: Otro nodo para comparar
            
        Returns:
            True si este nodo tiene menor frecuencia que el otro
        """
        return self.frecuencia < otro.frecuencia

def calcular_frecuencias(mensaje: str) -> defaultdict:
    """
    Calcula la frecuencia de cada carácter en el mensaje.
    
    Args:
        mensaje: El mensaje a analizar
        
    Returns:
        Diccionario con caracteres como claves y frecuencias como valores
    """
    frecuencias = defaultdict(int)
    for caracter in mensaje:
        frecuencias[caracter] += 1
    return frecuencias

def construir_arbol(frecuencias: dict) -> NodoArbol:
    """
    Construye el árbol de Huffman a partir de las frecuencias.
    
    Args:
        frecuencias: Diccionario de frecuencias de caracteres
        
    Returns:
        Raíz del árbol construido, o None si no hay frecuencias
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

def generar_codigos(raiz: NodoArbol, codigo_actual: str = "", codigos: dict = None) -> dict:
    """
    Genera los códigos de Huffman para cada carácter.
    
    Args:
        raiz: Raíz del árbol de Huffman
        codigo_actual: Código binario actual (para recursión)
        codigos: Diccionario de códigos (para recursión)
        
    Returns:
        Diccionario con caracteres como claves y códigos binarios como valores
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

def codificar_mensaje(mensaje: str, nombre_archivo: str) -> tuple:
    """
    Codifica un mensaje y lo guarda en un archivo .bin.
    
    Args:
        mensaje: El mensaje a codificar
        nombre_archivo: Ruta del archivo donde guardar
        
    Returns:
        Tupla con (raiz_arbol, codigos, bits_codificados)
        
    Raises:
        ValueError: Si el mensaje está vacío
        IOError: Si hay problemas al escribir el archivo
    """
    if not mensaje:
        raise ValueError("El mensaje no puede estar vacío")
    
    frecuencias = calcular_frecuencias(mensaje)

    raiz = construir_arbol(frecuencias)
    
    codigos = generar_codigos(raiz)
    
    bits = ''.join(codigos[caracter] for caracter in mensaje)
    
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(struct.pack('>I', len(frecuencias)))
        
        for caracter, freq in frecuencias.items():
            archivo.write(struct.pack('>cH', caracter.encode('utf-8'), freq))
        
        bits_restantes = len(bits) % 8
        bits_descartados = (8 - bits_restantes) % 8
        archivo.write(struct.pack('>B', bits_descartados))
        
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8].ljust(8, '0')
            archivo.write(bytes([int(byte, 2)]))
    
    return raiz, codigos, bits

def analizar_compresion(mensaje: str, codigos: dict) -> dict:
    """
    Analiza la compresión obtenida con los códigos de Huffman.
    
    Args:
        mensaje: Mensaje original
        codigos: Códigos de Huffman generados
        
    Returns:
        Diccionario con estadísticas de compresión
    """
    bits_original = len(mensaje) * 8  
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

def obtener_estadisticas_codificacion(mensaje: str, nombre_archivo: str) -> tuple:
    """
    Obtiene estadísticas completas de la codificación.
    
    Args:
        mensaje: Mensaje original
        nombre_archivo: Archivo donde se guardó
        
    Returns:
        Tupla con (estadisticas, raiz_arbol, codigos, bits)
    """

    raiz, codigos, bits = codificar_mensaje(mensaje, nombre_archivo)
    
    stats = analizar_compresion(mensaje, codigos)
    stats['archivo'] = nombre_archivo
    stats['tamaño_archivo'] = os.path.getsize(nombre_archivo)
    stats['caracteres_unicos'] = len(codigos)
    stats['bits_codificados'] = len(bits)
    
    return stats, raiz, codigos, bits

def mostrar_codigos(codigos: dict) -> None:
    """
    Muestra los códigos generados de forma ordenada.
    
    Args:
        codigos: Códigos de Huffman
    """
    print("Códigos de Huffman generados:")
    for caracter, codigo in sorted(codigos.items()):
        print(f"  '{caracter}': {codigo}")

def mostrar_estadisticas(stats: dict) -> None:
    """
    Muestra las estadísticas de compresión.
    
    Args:
        stats: Estadísticas de compresión
    """
    print(f"\nEstadísticas de compresión:")
    print(f"  Tamaño original: {stats['tamaño_original_bytes']} bytes")
    print(f"  Tamaño comprimido: {stats['tamaño_comprimido_bytes']} bytes")
    print(f"  Compresión: {stats['compresion_porcentaje']:.1f}%")
    print(f"  Ratio de compresión: {stats['ratio_compresion']:.2f}:1")

