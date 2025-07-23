# Documentación del Repositorio

Este repositorio contiene un analizador léxico y recursos asociados para el procesamiento de lenguajes de programación. A continuación se describe el propósito y contenido de cada archivo y carpeta.

---

## Estructura de Archivos y Carpetas

```
├── a_lexico.py
├── example.py
├── InstallationGuide.md
├── requirements.txt
├── diagrams/
│   ├── Flujo.wsd
│   ├── MotorTokens1.wsd
│   └── MotorTokens2.wsd
├── tests/
│   ├── escenarioPrueba1.txt
│   ├── escenarioPrueba1_lex.txt
│   ├── escenarioPrueba2.txt
│   ├── escenarioPrueba2_lex.txt
│   ├── escenarioPrueba3.txt
│   ├── escenarioPrueba3_lex.txt
│   ├── prototype1.txt
│   ├── prototype1_lex.txt
│   ├── prototype2.txt
│   ├── prototype2_lex.txt
│   ├── prototype3.txt
│   └── prototype3_lex.txt
└── .venv/
```

---

## Descripción de Archivos y Carpetas

### `a_lexico.py`
Implementa el **analizador léxico principal** usando la librería [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/). Define los tokens, palabras reservadas, tipos, literales, operadores, delimitadores y reglas para comentarios, identificadores y errores. Permite procesar archivos fuente y generar archivos de salida con los tokens reconocidos y su información (línea, posición, tipo, valor). Incluye un modo interactivo para pruebas.

### `example.py`
Ejemplo mínimo de un analizador léxico usando PLY. Reconoce números y operadores aritméticos básicos (`+`, `-`, `*`, `/`, `(`, `)`). Sirve como referencia didáctica para entender la estructura básica de un lexer con PLY.

### `InstallationGuide.md`
Guía paso a paso para la **instalación y configuración del entorno** de desarrollo. Incluye instrucciones para crear y activar un entorno virtual, instalar dependencias, registrar librerías y recomendaciones para el manejo de versiones y permisos.

### `requirements.txt`
Lista de dependencias del proyecto. Actualmente solo requiere:
- `ply==3.11`: Librería para construir analizadores léxicos y sintácticos en Python.

### Carpeta `diagrams/`
Contiene diagramas en formato PlantUML (`.wsd`) que ilustran el flujo y las reglas del motor de tokens:
- **Flujo.wsd**: Diagrama del flujo general del procesamiento léxico, desde la lectura del archivo hasta la salida de tokens.
- **MotorTokens1.wsd**: Diagrama de dependencias de reglas del motor de tokens para palabras reservadas, tipos, identificadores y literales numéricos.
- **MotorTokens2.wsd**: Diagrama de dependencias de reglas del motor de tokens para cadenas, caracteres, comentarios, operadores, delimitadores y manejo de errores.

### Carpeta `tests/`
Incluye archivos de **pruebas y escenarios de ejemplo**:
- Archivos `escenarioPruebaX.txt`: Casos de prueba con código fuente de entrada.
- Archivos `escenarioPruebaX_lex.txt`: Salida esperada del lexer para cada escenario.
- Archivos `prototypeX.txt` y `prototypeX_lex.txt`: Pruebas adicionales y prototipos de entrada/salida léxica.

### Carpeta `.venv/`
Directorio del entorno virtual de Python. **No debe subirse al repositorio** (añadir a `.gitignore`).

---

## Notas adicionales
- Para más detalles sobre la instalación, consulte `InstallationGuide.md`.
- Los diagramas `.wsd` pueden visualizarse con [PlantUML](https://plantuml.com/).
- El archivo principal para ejecutar el analizador léxico es `a_lexico.py`. 