# Taller 1: Analizador Léxico para Lenguaje de Pruebas Estadísticas

---

## 1. Introducción
- **Universidad:** Universidad Nacional de Colombia
- **Materia:** Lenguajes de Programación (2025966)
- **Fecha:** Junio 24 de 2025
- **Integrantes:**
  - Javier Andrés Tarazona Jiménez
  - David Felipe Marin Rosas
  - Juan Sebastian Muñoz Lemus
  - Eder José Hernández Buelvas
  - Axel Gomez Moreno
  - Daniel Santiago Delgado Pinilla
  
- **Tema:** Diseño e implementación de un analizador léxico (lexer) para un lenguaje de programación específico.
- **Aplicación:** Pruebas estadísticas tipo Friedman y análisis de rachas.
- **Herramienta:** Python + PLY.


---

## 2. Motivación y Justificación
- Estadísticos requieren herramientas especializadas.
- Lenguajes generales (R, Python, MATLAB) son complejos para usuarios no expertos.
- Un DSL (lenguaje específico) simplifica y reduce errores en análisis estadístico.

---

## 3. Objetivos
- **General:**
  - Construir el analizador léxico para un lenguaje orientado a pruebas estadísticas.
- **Específicos:**
  - Prototipar programas ejemplo.
  - Definir vocabulario y categorías léxicas.
  - Formalizar patrones con expresiones regulares.
  - Implementar el lexer con PLY.

---

## 4. Diseño de la Solución
- **Pipeline modular de 6 capas:**
  1. Lector de archivo
  2. Preprocesamiento
  3. Construcción del lexer (PLY)
  4. Motor de tokenización
  5. Salida de tokens
  6. Integración para fases posteriores
- **Diagrama:**
  - Imagen del flujo modular (ver Flujo.png)

---

## 5. Categorías Léxicas Definidas
- Palabras clave (Func, Principal, Si, Entonces, etc.)
- Tipos de datos (Entero, Flotante, Bool, etc.)
- Tipos abstractos (Arreglo, Matriz, Conjunto, etc.)
- Identificadores
- Literales (enteros, reales, complejos, cadenas, caracteres)
- Operadores (aritméticos, lógicos, relacionales, asignación)
- Delimitadores ({}, (), [], ,, ;, .)
- Comentarios (//, /* */)

---

## 6. Implementación Técnica
- **PLY (Python Lex-Yacc):**
  - Definición de tokens y expresiones regulares.
  - Diccionario de palabras reservadas.
  - Funciones para cada token.
  - Manejo de errores léxicos.
- **Entrada/Salida:**
  - Lee archivo fuente, genera archivo de tokens con tipo, valor, línea y posición.

---

## 7. Manual de Usuario
- Crear entorno virtual y activar.
- Instalar dependencias (`pip install -r requirements.txt`).
- Ejecutar: `python a_lexico.py`.
- Ingresar ruta del archivo fuente.
- Se genera archivo de salida con tokens.

---

## 8. Pruebas y Experimentación
- **Escenario 1:** Código correcto (todas las categorías léxicas).
- **Escenario 2:** Código con errores léxicos (robustez y tolerancia a fallos).
- **Escenario 3:** Anidamientos complejos (tipos genéricos, funciones anidadas).
- **Resultados:**
  - Lexer reconoce correctamente tokens válidos.
  - Reporta errores y continúa análisis.

---

## 9. Conclusiones
- El analizador léxico es robusto y modular.
- Reconoce todas las estructuras del lenguaje propuesto.
- Base sólida para etapas posteriores (parser, semántica).
- Facilita el análisis estadístico especializado.

---

## 10. Reflexiones y Mejoras Futuras
- Mejorar mensajes de error (línea, columna).
- Automatizar pruebas unitarias.
- Visualización de tokens y métricas.


---

¡Gracias!
¿Preguntas?

## Referencias
- J. R. Levine, T. Mason, and D. Brown, “Lex & Yacc,” 2nd ed., O’Reilly & Associates, 1992.
- D. M. Beazley, “PLY (Python Lex‐Yacc) Manual,” Version 3.11, 2023. [Online]. Disponible en: https://www.dabeaz.com/ply/
- J. E. Ortiz Triviño, "Lenguaje para procesamiento de rachas," Documento interno, Universidad Nacional de Colombia, enviado por correo electrónico, 6 de mayo de 2025. 