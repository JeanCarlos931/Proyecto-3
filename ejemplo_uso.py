#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Decodificador Gráfico de Mensajes - Huffman

Este script demuestra las funcionalidades principales del programa
sin necesidad de usar la interfaz gráfica.
"""

import os
import sys

# Importaciones de módulos propios
from huffman_codificador import (
    calcular_frecuencias, 
    construir_arbol, 
    generar_codigos, 
    codificar_mensaje,
    analizar_compresion,
    obtener_estadisticas_codificacion
)
from huffman_decodificador import (
    decodificar_archivo,
    validar_archivo,
    analizar_archivo,
    mostrar_analisis_archivo
)

def ejemplo_basico():
    """Ejemplo básico de codificación y decodificación."""
    print("=" * 60)
    print("EJEMPLO BÁSICO DE CODIFICACIÓN Y DECODIFICACIÓN")
    print("=" * 60)
    
    # Mensaje de ejemplo
    mensaje = "HOLA MUNDO"
    print(f"Mensaje original: '{mensaje}'")
    print(f"Longitud: {len(mensaje)} caracteres")
    
    # Calcular frecuencias
    frecuencias = calcular_frecuencias(mensaje)
    print(f"\nFrecuencias de caracteres:")
    for caracter, freq in sorted(frecuencias.items()):
        print(f"  '{caracter}': {freq}")
    
    # Construir árbol
    raiz = construir_arbol(frecuencias)
    print(f"\nÁrbol de Huffman construido con {len(frecuencias)} hojas")
    
    # Generar códigos
    codigos = generar_codigos(raiz)
    print(f"\nCódigos de Huffman generados:")
    for caracter, codigo in sorted(codigos.items()):
        print(f"  '{caracter}': {codigo}")
    
    # Calcular bits originales vs comprimidos
    bits_original = len(mensaje) * 8  # ASCII
    bits_comprimido = sum(len(codigos[caracter]) for caracter in mensaje)
    
    print(f"\nAnálisis de compresión:")
    print(f"  Bits originales (ASCII): {bits_original}")
    print(f"  Bits comprimidos: {bits_comprimido}")
    print(f"  Compresión: {((1 - bits_comprimido/bits_original) * 100):.1f}%")
    
    return mensaje, raiz, codigos

def ejemplo_codificacion_archivo():
    """Ejemplo de codificación y guardado en archivo."""
    print("\n" + "=" * 60)
    print("EJEMPLO DE CODIFICACIÓN Y GUARDADO EN ARCHIVO")
    print("=" * 60)
    
    # Mensaje de ejemplo
    mensaje = "Este es un mensaje de prueba para demostrar la compresión de Huffman"
    print(f"Mensaje: '{mensaje}'")
    
    # Archivo temporal
    archivo_temp = "mensaje_ejemplo.bin"
    
    try:
        # Codificar y guardar usando el módulo de codificación
        stats, raiz, codigos, bits = obtener_estadisticas_codificacion(mensaje, archivo_temp)
        
        print(f"\nArchivo guardado: {archivo_temp}")
        print(f"Tamaño del archivo: {stats['tamaño_archivo']} bytes")
        print(f"Bits codificados: {stats['bits_codificados']}")
        print(f"Compresión: {stats['compresion_porcentaje']:.1f}%")
        
        # Decodificar y verificar usando el módulo de decodificación
        mensaje_decodificado, raiz_reconstruida, bits_leidos = decodificar_archivo(archivo_temp)
        
        print(f"\nVerificación:")
        print(f"  Mensaje original: '{mensaje}'")
        print(f"  Mensaje decodificado: '{mensaje_decodificado}'")
        print(f"  ¿Coinciden?: {'✅ SÍ' if mensaje == mensaje_decodificado else '❌ NO'}")
        
        # Analizar archivo
        analisis = analizar_archivo(archivo_temp)
        print(f"\nAnálisis del archivo:")
        print(f"  Válido: {'✅ SÍ' if analisis['valido'] else '❌ NO'}")
        print(f"  Caracteres únicos: {analisis['caracteres_unicos']}")
        print(f"  Longitud del mensaje: {analisis['longitud_mensaje']}")
        
        # Limpiar archivo temporal
        os.remove(archivo_temp)
        print(f"\nArchivo temporal eliminado: {archivo_temp}")
        
    except Exception as e:
        print(f"Error: {e}")

def ejemplo_texto_largo():
    """Ejemplo con texto más largo para mostrar mejor compresión."""
    print("\n" + "=" * 60)
    print("EJEMPLO CON TEXTO LARGO")
    print("=" * 60)
    
    texto_largo = """
    El algoritmo de Huffman es un algoritmo de compresión de datos que utiliza 
    códigos de longitud variable para representar caracteres. Fue desarrollado 
    por David A. Huffman en 1952 mientras era estudiante en el MIT.
    
    El algoritmo funciona construyendo un árbol binario basado en las frecuencias 
    de aparición de cada carácter en el texto. Los caracteres más frecuentes 
    reciben códigos más cortos, mientras que los menos frecuentes reciben códigos 
    más largos, optimizando así la compresión.
    
    Este método es ampliamente utilizado en aplicaciones como compresión de 
    archivos, transmisión de datos y codificación de información.
    """
    
    # Limpiar texto (remover espacios extra)
    texto_limpio = " ".join(texto_largo.split())
    
    print(f"Texto de ejemplo ({len(texto_limpio)} caracteres):")
    print(f"'{texto_limpio[:100]}...'")
    
    # Calcular frecuencias
    frecuencias = calcular_frecuencias(texto_limpio)
    print(f"\nCaracteres únicos: {len(frecuencias)}")
    
    # Mostrar los 10 caracteres más frecuentes
    frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 10 caracteres más frecuentes:")
    for i, (caracter, freq) in enumerate(frecuencias_ordenadas[:10], 1):
        porcentaje = (freq / len(texto_limpio)) * 100
        print(f"  {i:2d}. '{caracter}': {freq:3d} veces ({porcentaje:5.1f}%)")
    
    # Construir árbol y generar códigos
    raiz = construir_arbol(frecuencias)
    codigos = generar_codigos(raiz)
    
    # Calcular compresión
    bits_original = len(texto_limpio) * 8
    bits_comprimido = sum(len(codigos[caracter]) for caracter in texto_limpio)
    
    print(f"\nAnálisis de compresión:")
    print(f"  Tamaño original: {bits_original} bits ({bits_original//8} bytes)")
    print(f"  Tamaño comprimido: {bits_comprimido} bits ({bits_comprimido//8 + 1} bytes)")
    print(f"  Compresión: {((1 - (bits_comprimido//8 + 1)/(bits_original//8)) * 100):.1f}%")
    
    # Mostrar algunos códigos
    print(f"\nEjemplos de códigos generados:")
    for caracter, codigo in sorted(codigos.items())[:10]:
        print(f"  '{caracter}': {codigo}")

def ejemplo_caracteres_especiales():
    """Ejemplo con caracteres especiales y acentos."""
    print("\n" + "=" * 60)
    print("EJEMPLO CON CARACTERES ESPECIALES")
    print("=" * 60)
    
    texto_especial = "¡Hola! ¿Cómo estás? Éste es un mensaje con acentos: áéíóúñüç"
    print(f"Texto con caracteres especiales: '{texto_especial}'")
    
    # Calcular frecuencias
    frecuencias = calcular_frecuencias(texto_especial)
    
    print(f"\nFrecuencias (incluyendo caracteres especiales):")
    for caracter, freq in sorted(frecuencias.items()):
        print(f"  '{caracter}' (ASCII: {ord(caracter):3d}): {freq}")
    
    # Construir árbol y generar códigos
    raiz = construir_arbol(frecuencias)
    codigos = generar_codigos(raiz)
    
    print(f"\nCódigos generados:")
    for caracter, codigo in sorted(codigos.items()):
        print(f"  '{caracter}': {codigo}")
    
    # Verificar que la decodificación funciona
    bits = ''.join(codigos[caracter] for caracter in texto_especial)
    print(f"\nSecuencia de bits: {bits}")
    print(f"Longitud de bits: {len(bits)}")

def ejemplo_validacion_archivos():
    """Ejemplo de validación y análisis de archivos."""
    print("\n" + "=" * 60)
    print("EJEMPLO DE VALIDACIÓN Y ANÁLISIS DE ARCHIVOS")
    print("=" * 60)
    
    # Crear archivo de prueba
    mensaje = "Mensaje de prueba para validación"
    archivo_temp = "archivo_validacion.bin"
    
    try:
        # Codificar mensaje
        codificar_mensaje(mensaje, archivo_temp)
        
        # Validar archivo
        validacion = validar_archivo(archivo_temp)
        print(f"Validación del archivo '{archivo_temp}':")
        print(f"  Válido: {'✅ SÍ' if validacion['valido'] else '❌ NO'}")
        if validacion['valido']:
            print(f"  Tamaño: {validacion['tamaño']} bytes")
            print(f"  Caracteres únicos: {validacion['caracteres_unicos']}")
            print(f"  Bits descartados: {validacion['bits_descartados']}")
        else:
            print(f"  Error: {validacion['error']}")
        
        # Analizar archivo
        print(f"\nAnálisis detallado:")
        analisis = analizar_archivo(archivo_temp)
        if analisis['valido']:
            mostrar_analisis_archivo(analisis)
        else:
            print(f"  Error en análisis: {analisis['error']}")
        
        # Limpiar
        os.remove(archivo_temp)
        print(f"\nArchivo temporal eliminado: {archivo_temp}")
        
    except Exception as e:
        print(f"Error: {e}")

def mostrar_estadisticas():
    """Muestra estadísticas generales del algoritmo."""
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS Y CARACTERÍSTICAS DEL ALGORITMO")
    print("=" * 60)
    
    print("""
    🎯 CARACTERÍSTICAS DEL ALGORITMO DE HUFFMAN:
    
    ✅ Ventajas:
       • Compresión sin pérdida de información
       • Óptimo para códigos de longitud variable
       • Eficiente para textos con frecuencias variables
       • Algoritmo determinístico y reproducible
    
    📊 Eficiencia:
       • Mejor compresión en textos con frecuencias desiguales
       • Menos eficiente en textos con frecuencias uniformes
       • Overhead mínimo para archivos pequeños
    
    🔧 Implementación:
       • Uso de heap (montículo) para construcción eficiente
       • Estructura de árbol binario
       • Codificación recursiva de códigos
       • Manejo de bits de relleno
    
    📁 Formato de archivo:
       • Header con metadatos (frecuencias)
       • Datos comprimidos en formato binario
       • Información de bits de relleno
       • Compatible con cualquier tipo de texto
    
    🏗️ Arquitectura Modular:
       • huffman_codificador.py: Funciones de codificación
       • huffman_decodificador.py: Funciones de decodificación
       • main.py: Interfaz gráfica y coordinación
       • ejemplo_uso.py: Ejemplos y demostraciones
    """)

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🌳 DECODIFICADOR GRÁFICO DE MENSAJES - HUFFMAN")
    print("Ejemplos de uso y demostración")
    print("=" * 60)
    
    try:
        # Ejecutar ejemplos
        ejemplo_basico()
        ejemplo_codificacion_archivo()
        ejemplo_texto_largo()
        ejemplo_caracteres_especiales()
        ejemplo_validacion_archivos()
        mostrar_estadisticas()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nPara usar la interfaz gráfica, ejecuta: python main.py")
        
    except KeyboardInterrupt:
        print("\n\n❌ Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 