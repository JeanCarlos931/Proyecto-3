import struct
import os
from codificador import NodoArbol, construir_arbol

def leer_metadatos_archivo(nombre_archivo: str) -> tuple:
    """
    Lee los metadatos del archivo .bin (frecuencias y bits descartados).
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        
    Returns:
        Tupla con (frecuencias, bits_descartados, posicion_datos)
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está corrupto
    """
    if not os.path.exists(nombre_archivo):
        raise FileNotFoundError(f"El archivo '{nombre_archivo}' no existe")
    
    with open(nombre_archivo, 'rb') as archivo:
        try:
            datos = archivo.read(4)
            if len(datos) < 4:
                raise ValueError("Archivo corrupto: no se puede leer el número de caracteres")
            
            num_caracteres = struct.unpack('>I', datos)[0]
            
            frecuencias = {}
            for _ in range(num_caracteres):
                datos = archivo.read(3)
                if len(datos) < 3:
                    raise ValueError("Archivo corrupto: datos de frecuencias incompletos")
                
                caracter, freq = struct.unpack('>cH', datos)
                frecuencias[caracter.decode('utf-8')] = freq
            
            datos = archivo.read(1)
            if len(datos) < 1:
                raise ValueError("Archivo corrupto: no se puede leer bits descartados")
            
            bits_descartados = struct.unpack('>B', datos)[0]
            
            posicion_datos = archivo.tell()
            
            return frecuencias, bits_descartados, posicion_datos
            
        except struct.error as e:
            raise ValueError(f"Archivo corrupto: error al leer estructura de datos - {e}")

def leer_datos_codificados(nombre_archivo: str, posicion_inicio: int) -> str:
    """
    Lee los datos codificados del archivo.
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        posicion_inicio: Posición donde comienzan los datos
        
    Returns:
        Secuencia de bits como string
    """
    with open(nombre_archivo, 'rb') as archivo:
        archivo.seek(posicion_inicio)
        datos = archivo.read()
        
        bits = ''.join(f'{byte:08b}' for byte in datos)
        return bits
    
def reconstruir_arbol_desde_archivo(nombre_archivo: str) -> NodoArbol:
    """
    Reconstruye el árbol de Huffman desde un archivo .bin.
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        
    Returns:
        Raíz del árbol reconstruido
    """
    frecuencias, _, _ = leer_metadatos_archivo(nombre_archivo)
    return construir_arbol(frecuencias)

def decodificar_bits(bits: str, raiz: NodoArbol) -> str:
    """
    Decodifica una secuencia de bits usando el árbol de Huffman.
    
    Args:
        bits: Secuencia de bits a decodificar
        raiz: Raíz del árbol de Huffman
        
    Returns:
        Mensaje decodificado
    """
    if not bits or raiz is None:
        return ""
    
    mensaje = []
    nodo_actual = raiz
    
    for bit in bits:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        
        if nodo_actual.caracter is not None:
            mensaje.append(nodo_actual.caracter)
            nodo_actual = raiz 
    
    return ''.join(mensaje)

def decodificar_archivo(nombre_archivo: str) -> tuple:
    """
    Decodifica un archivo .bin completo.
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        
    Returns:
        Tupla con (mensaje_decodificado, raiz_arbol, bits_leidos)
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está corrupto
    """

    frecuencias, bits_descartados, posicion_datos = leer_metadatos_archivo(nombre_archivo)
    
    bits_completos = leer_datos_codificados(nombre_archivo, posicion_datos)
    
    if bits_descartados > 0:
        bits_completos = bits_completos[:-bits_descartados]
    
    raiz = construir_arbol(frecuencias)
    
    mensaje = decodificar_bits(bits_completos, raiz)
    
    return mensaje, raiz, bits_completos

def decodificar_paso_a_paso(bits: str, raiz: NodoArbol):
    """
    Decodifica bits paso a paso, retornando cada paso del proceso.
    
    Args:
        bits: Secuencia de bits a decodificar
        raiz: Raíz del árbol de Huffman
        
    Yields:
        Diccionario con información de cada paso (nodo_actual, bit, caracter_encontrado, mensaje_parcial)
    """
    if not bits or raiz is None:
        return
    
    mensaje_parcial = []
    nodo_actual = raiz
    
    for i, bit in enumerate(bits):
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        
        paso = {
            'indice_bit': i,
            'bit': bit,
            'nodo_actual': nodo_actual,
            'caracter_encontrado': None,
            'mensaje_parcial': ''.join(mensaje_parcial),
            'es_hoja': nodo_actual.caracter is not None
        }
        
        if nodo_actual.caracter is not None:
            mensaje_parcial.append(nodo_actual.caracter)
            paso['caracter_encontrado'] = nodo_actual.caracter
            paso['mensaje_parcial'] = ''.join(mensaje_parcial)
            nodo_actual = raiz
        
        yield paso

def validar_archivo(nombre_archivo: str) -> dict:
    """
    Valida que un archivo .bin sea válido y no esté corrupto.
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        
    Returns:
        Diccionario con información de validación
    """
    try:
        if not os.path.exists(nombre_archivo):
            return {
                'valido': False,
                'error': 'Archivo no encontrado'
            }
        
        tamaño = os.path.getsize(nombre_archivo)
        if tamaño < 5: 
            return {
                'valido': False,
                'error': 'Archivo demasiado pequeño'
            }
        
        frecuencias, bits_descartados, posicion_datos = leer_metadatos_archivo(nombre_archivo)
        
        if posicion_datos >= tamaño:
            return {
                'valido': False,
                'error': 'No hay datos codificados'
            }
        
        return {
            'valido': True,
            'tamaño': tamaño,
            'caracteres_unicos': len(frecuencias),
            'bits_descartados': bits_descartados,
            'tamaño_datos': tamaño - posicion_datos
        }
        
    except Exception as e:
        return {
            'valido': False,
            'error': str(e)
        }

def verificar_integridad(mensaje_original: str, nombre_archivo: str) -> dict:
    """
    Verifica la integridad de un archivo decodificándolo y comparándolo.
    
    Args:
        mensaje_original: Mensaje original que se codificó
        nombre_archivo: Archivo .bin a verificar
        
    Returns:
        Diccionario con resultado de la verificación
    """
    try:
        mensaje_decodificado, _, _ = decodificar_archivo(nombre_archivo)
        
        return {
            'coincide': mensaje_original == mensaje_decodificado,
            'mensaje_original': mensaje_original,
            'mensaje_decodificado': mensaje_decodificado,
            'longitud_original': len(mensaje_original),
            'longitud_decodificado': len(mensaje_decodificado)
        }
        
    except Exception as e:
        return {
            'coincide': False,
            'error': str(e)
        }

def analizar_archivo(nombre_archivo: str) -> dict:
    """
    Analiza un archivo .bin y proporciona información detallada.
    
    Args:
        nombre_archivo: Ruta del archivo .bin
        
    Returns:
        Diccionario con información detallada del archivo
    """
    try:
        # Validar archivo
        validacion = validar_archivo(nombre_archivo)
        if not validacion['valido']:
            return validacion
        
        # Leer metadatos
        frecuencias, bits_descartados, posicion_datos = leer_metadatos_archivo(nombre_archivo)
        
        # Leer datos
        bits = leer_datos_codificados(nombre_archivo, posicion_datos)
        if bits_descartados > 0:
            bits = bits[:-bits_descartados]
        
        # Reconstruir árbol
        raiz = construir_arbol(frecuencias)
        
        # Decodificar
        mensaje = decodificar_bits(bits, raiz)
        
        return {
            'valido': True,
            'tamaño_archivo': os.path.getsize(nombre_archivo),
            'caracteres_unicos': len(frecuencias),
            'frecuencias': frecuencias,
            'bits_descartados': bits_descartados,
            'bits_codificados': len(bits),
            'mensaje_decodificado': mensaje,
            'longitud_mensaje': len(mensaje),
            'tamaño_metadatos': posicion_datos,
            'tamaño_datos': len(bits) // 8 + 1
        }
        
    except Exception as e:
        return {
            'valido': False,
            'error': str(e)
        }

def mostrar_analisis_archivo(analisis: dict) -> None:
    """
    Muestra el análisis de un archivo de forma legible.
    
    Args:
        analisis: Resultado de analizar_archivo()
    """
    if not analisis['valido']:
        print(f"❌ Archivo inválido: {analisis['error']}")
        return
    
    print("📊 ANÁLISIS DEL ARCHIVO")
    print("=" * 40)
    print(f"Tamaño del archivo: {analisis['tamaño_archivo']} bytes")
    print(f"Caracteres únicos: {analisis['caracteres_unicos']}")
    print(f"Bits codificados: {analisis['bits_codificados']}")
    print(f"Bits descartados: {analisis['bits_descartados']}")
    print(f"Longitud del mensaje: {analisis['longitud_mensaje']} caracteres")
    print(f"Mensaje: '{analisis['mensaje_decodificado']}'")
    
    print(f"\nFrecuencias de caracteres:")
    for caracter, freq in sorted(analisis['frecuencias'].items()):
        print(f"  '{caracter}': {freq}")
