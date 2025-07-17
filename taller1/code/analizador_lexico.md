# Documentación detallada de `a_lexico.py`

Este archivo implementa un **analizador léxico** en Python utilizando la librería [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/). Su objetivo es identificar y clasificar los distintos elementos léxicos (tokens) de un lenguaje de programación personalizado.

---

## Estructura General

- **Definición de tokens**: Palabras reservadas, tipos, identificadores, literales, operadores, delimitadores, comentarios, etc.
- **Expresiones regulares**: Para cada tipo de token.
- **Funciones de acción**: Asociadas a cada token para procesar y devolver información relevante.
- **Manejo de errores**: Para caracteres inesperados.
- **Modo interactivo y procesamiento de archivos**: Permite analizar archivos fuente y generar archivos de salida con los tokens reconocidos.

---

## Componentes Principales

### 1. Importaciones
- `re`: Módulo de expresiones regulares de Python.
- `ply.lex as lex`: Módulo de PLY para construir analizadores léxicos.

### 2. Lista de tokens
- Se define la lista `tokens` que contiene todos los tipos de elementos léxicos reconocidos.

### 3. Palabras reservadas y tipos
- **Palabras reservadas**: Ej. `Func`, `Principal`, `imprimir`, etc. Se almacenan en `palabras_reservadas` y se agregan al diccionario `reserved`.
- **Tipos**: Se distinguen dos grupos: `TIPOA` (tipos primitivos como `Bool`, `Entero`, etc.) y `TIPOB` (estructuras como `Conjunto`, `Arreglo`, etc.).

### 4. Tokens para cadenas y caracteres
- **CARACTER**: Expresión regular para un carácter entre comillas simples.
- **CADENA**: Expresiones regulares para cadenas normales y cadenas formateadas (f-strings).

### 5. Identificadores y booleanos
- **ID**: Identificadores válidos del lenguaje.
- **BOOL**: Palabras reservadas `Verdadero` y `Falso`.

### 6. Literales numéricos
- **ENTERO**: Números enteros.
- **REAL**: Números reales (flotantes).
- **COMPLEJO**: Números complejos (con parte imaginaria).

### 7. Comentarios
- **COMMENT**: Soporta comentarios de línea (`// ...`) y de bloque (`/* ... */`).

### 8. Operadores y delimitadores
- **OPREL**: Operadores relacionales (`<`, `>`, `==`, etc.).
- **OPASI**: Operadores de asignación (`=`, `+=`, etc.).
- **OPASIU**: Operadores de asignación unaria (`++`, `--`).
- **OPACC**: Operadores de acceso (`[`, `]`, `.`).
- **OPARIT**: Operadores aritméticos (`+`, `-`, `*`, `/`, etc.).
- **OPLOG**: Operadores lógicos (`&&`, `||`, `NO`, `Y`, `O`, `!`).
- **DELIM**: Delimitadores (`;`, `{`, `}`, `,`, `(`, `)`).

### 9. Espacios y saltos de línea
- Se ignoran espacios y tabulaciones (`t_ignore = ' \t'`).
- Se actualiza el número de línea con saltos (`t_newline`).

### 10. Manejo de errores
- La función `t_error` captura caracteres no reconocidos e imprime un mensaje de error.

### 11. Construcción del lexer
- Se construye el lexer con `lex.lex(reflags=lex.re.VERBOSE)` para permitir expresiones regulares legibles.

### 12. Ejecución como script principal
- Si se ejecuta directamente, permite ingresar el nombre de un archivo fuente, lo analiza y genera un archivo de salida con los tokens reconocidos y su información (línea, posición, tipo, valor).
- Incluye manejo de errores para archivos no encontrados.

---

## Ejemplo de uso

```bash
python a_lexico.py
# Luego ingresar el nombre del archivo fuente a analizar (por ejemplo: ejemplo.txt)
# Se generará un archivo ejemplo_lex.txt con la salida léxica.
```

---

## Notas adicionales
- El archivo está preparado para ser extendido fácilmente con nuevos tokens o reglas.
- Los comentarios y la estructura facilitan la comprensión y modificación del analizador.
- Utiliza expresiones regulares avanzadas para soportar características modernas del lenguaje (como f-strings y comentarios multilínea). 