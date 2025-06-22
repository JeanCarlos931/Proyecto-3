# 🌳 Decodificador Gráfico de Mensajes - Huffman

Una aplicación completa en Python que implementa el algoritmo de compresión de Huffman con visualización gráfica interactiva del árbol binario y animación paso a paso de la decodificación.

## 🚀 Características

### Funcionalidades Principales

- **Codificación de Mensajes**: Convierte texto plano en archivos binarios comprimidos
- **Decodificación Visual**: Reconstruye mensajes con animación paso a paso
- **Visualización Gráfica**: Muestra el árbol de Huffman de forma interactiva
- **Interfaz Amigable**: GUI moderna con Tkinter

### Algoritmo de Huffman

- Construcción automática del árbol de Huffman
- Cálculo de frecuencias de caracteres
- Generación de códigos óptimos
- Compresión eficiente de datos

### Visualización Interactiva

- **Árbol Binario**: Representación gráfica del árbol de Huffman
- **Animación Paso a Paso**: Recorrido visual bit por bit
- **Resaltado Dinámico**: Nodos activos se resaltan durante la decodificación
- **Controles de Animación**: Iniciar, pausar, reiniciar y limpiar

## 📁 Estructura del Proyecto

```
Turing's foster/
├── main.py          # Aplicación principal
├── cursor.py        # Archivo auxiliar
└── README.md        # Documentación
```

## 🛠️ Requisitos

- Python 3.6 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)
- Bibliotecas estándar de Python:
  - `heapq`
  - `struct`
  - `collections`
  - `os`

## 🚀 Instalación y Uso

### 1. Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd "Turing's foster"
```

### 2. Ejecutar la Aplicación

```bash
python main.py
```

### 3. Usar la Interfaz

1. **Codificar un Mensaje**:
   - Hacer clic en "📝 Codificar Mensaje"
   - Ingresar el texto a comprimir
   - Seleccionar ubicación del archivo .bin
   - Ver estadísticas de compresión

2. **Decodificar un Archivo**:
   - Hacer clic en "🔍 Decodificar Archivo"
   - Seleccionar archivo .bin
   - Ver el mensaje reconstruido
   - Observar la animación del árbol

## 📊 Formato del Archivo Binario

El archivo `.bin` generado tiene la siguiente estructura:

```
[4 bytes]  Número de caracteres únicos
[n × 3 bytes]  Secuencia de caracteres y frecuencias
[1 byte]   Bits descartados en el último byte
[bytes]    Secuencia de bits codificados
```

### Detalles de la Estructura:

- **4 bytes iniciales**: Cantidad de caracteres únicos (big-endian)
- **3 bytes por carácter**: 1 byte para el carácter + 2 bytes para frecuencia
- **1 byte de control**: Bits de relleno descartados
- **Datos codificados**: Secuencia de bits del mensaje comprimido

## 🎨 Características de la Visualización

### Colores del Árbol

- **Azul claro** (`#E3F2FD`): Nodos internos
- **Verde claro** (`#C8E6C9`): Hojas (caracteres)
- **Amarillo** (`#FFEB3B`): Nodo activo durante animación
- **Verde** (`#4CAF50`): Hoja encontrada

### Controles de Animación

- **▶ Iniciar**: Comienza la decodificación paso a paso
- **⏸ Pausar**: Detiene temporalmente la animación
- **🔄 Reiniciar**: Vuelve al inicio de la decodificación
- **🗑 Limpiar**: Cierra la ventana de visualización

### Información en Tiempo Real

- Progreso de bits procesados
- Caracteres decodificados
- Mensaje reconstruido
- Estadísticas de compresión

## 🔧 Funciones Técnicas

### Clases Principales

#### `NodoHuffman`
```python
class NodoHuffman:
    __slots__ = ('caracter', 'frecuencia', 'izquierda', 'derecha')
```
Representa un nodo del árbol de Huffman.

#### `VisualizadorHuffman`
```python
class VisualizadorHuffman:
    def __init__(self, raiz, bits="")
```
Maneja la visualización gráfica y animación.

#### `InterfazPrincipal`
```python
class InterfazPrincipal:
    def __init__(self)
```
Interfaz principal de la aplicación.

### Funciones de Codificación

- `calcular_frecuencias(mensaje)`: Analiza frecuencias de caracteres
- `construir_arbol(frecuencias)`: Construye el árbol de Huffman
- `generar_codigos(raiz)`: Genera códigos binarios para cada carácter
- `codificar_mensaje(mensaje, archivo)`: Codifica y guarda en archivo

### Funciones de Decodificación

- `decodificar_archivo(archivo)`: Lee y decodifica archivo .bin
- `animar_paso()`: Ejecuta un paso de la animación
- `resaltar_nodo(nodo, color)`: Resalta nodos durante animación

## 📈 Ejemplo de Uso

### Codificación
```
Mensaje: "HOLA MUNDO"
Frecuencias: {'H': 1, 'O': 2, 'L': 1, 'A': 1, ' ': 1, 'M': 1, 'U': 1, 'N': 1, 'D': 1}
Códigos: {'H': '000', 'O': '01', 'L': '001', 'A': '100', ' ': '101', 'M': '110', 'U': '1110', 'N': '1111', 'D': '1100'}
```

### Compresión
- **Original**: 10 caracteres = 80 bits (ASCII)
- **Comprimido**: ~35 bits
- **Compresión**: ~56%

## 🎯 Características Avanzadas

### Optimizaciones Implementadas

- **Uso de `__slots__`**: Mejora el rendimiento de memoria
- **Estructuras de datos eficientes**: Heap para construcción del árbol
- **Manejo de errores robusto**: Validaciones y excepciones
- **Interfaz responsiva**: Adaptación automática al tamaño de ventana

### Extras Opcionales

- **Estadísticas detalladas**: Información de compresión
- **Controles de animación**: Pausa, reinicio, limpieza
- **Visualización mejorada**: Colores, etiquetas, flechas
- **Documentación integrada**: Comentarios y docstrings

## 🐛 Solución de Problemas

### Errores Comunes

1. **"No hay bits para decodificar"**
   - Verificar que el archivo .bin sea válido
   - Asegurar que el archivo no esté corrupto

2. **"Error al codificar el mensaje"**
   - Verificar que el mensaje no esté vacío
   - Comprobar permisos de escritura en el directorio

3. **Problemas de visualización**
   - Asegurar que Tkinter esté instalado
   - Verificar resolución de pantalla

### Debugging

Para activar modo debug, agregar al inicio de `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📞 Contacto

Para preguntas o sugerencias, por favor abrir un issue en el repositorio.

---

**Desarrollado con ❤️ usando Python y Tkinter** 