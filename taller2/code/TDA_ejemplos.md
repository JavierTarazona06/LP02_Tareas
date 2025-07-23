# Ejemplos de Tipos Abstractos de Datos (TDA)

A continuación se muestran ejemplos de cómo se verían instancias de los tipos abstractos definidos en `TDA.py`, incluyendo sus atributos principales y ejemplos de contenido.

---

## 1. `Cadena`

**Descripción:** Representa una cadena de caracteres.

```python
Cadena("hola mundo")
# value: "hola mundo"
```

---

## 2. `Arreglo`

**Descripción:** Estructura de datos tipo arreglo (vector), homogéneo en su tipo de dato.

```python
Arreglo(int)
# data: [1, 2, 3, 4, 5]

Arreglo(Cadena)
# data: [Cadena("a"), Cadena("b"), Cadena("c")]

Arreglo(Arreglo)
# data: [Arreglo(int) [1,2], Arreglo(int) [3,4]]
```

---

## 3. `Conjunto`

**Descripción:** Estructura de datos tipo conjunto, sin elementos repetidos.

```python
Conjunto(int)
# data: [1, 2, 3]

Conjunto(Cadena)
# data: [Cadena("x"), Cadena("y")]
```

---

## 4. `Diccionario`

**Descripción:** Diccionario con tipos de clave y valor definidos.

```python
Diccionario(str, int)
# data: {"a": 1, "b": 2}

Diccionario(Cadena, Arreglo)
# data: {Cadena("letras"): Arreglo(Cadena) [Cadena("a"), Cadena("b")], Cadena("nums"): Arreglo(int) [1,2,3]}
```

---

## 5. `Matriz`

**Descripción:** Matriz de tamaño fijo, homogénea en su tipo de dato.

```python
Matriz(2, 3, float)
# filas: 2
# columnas: 3
# datatype: float
# data:
# [ [1.1, 2.2, 3.3],
#   [4.4, 5.5, 6.6] ]

Matriz(3, 2, Cadena)
# data:
# [ [Cadena("a"), Cadena("b")],
#   [Cadena("c"), Cadena("d")],
#   [Cadena("e"), Cadena("f")] ]
```

---

## 6. `MatrizRachas`

**Descripción:** Matriz donde cada celda contiene una cadena de rachas (Cadena).

```python
MatrizRachas(bloques=["B1", "B2"], tratamientos=["T1", "T2"])
# data:
# [ [Cadena("AAABBB"), Cadena("ABAB")],
#   [Cadena("BBBB"),   Cadena("AABB")] ]
# bloques: ["B1", "B2"]
# tratamientos: ["T1", "T2"]
```

---

## 7. `Multicotomizacion`

**Descripción:** Modelo de multicotomización con categorías y reglas.

```python
Multicotomizacion(categorias=Conjunto(Cadena) [Cadena("A"), Cadena("B")], datatype=int)
# reglas: [ (lambda x: x > 0, "A"), (lambda x: x <= 0, "B") ]
```

---

## 8. `M2VClasificacion`

**Descripción:** Modelo de clasificación con matriz de arreglos.

```python
M2VClasificacion(paramGlobal=0.5, bloques=Arreglo(Cadena) [Cadena("B1"), Cadena("B2")], tratamientos=Arreglo(Cadena) [Cadena("T1"), Cadena("T2")], datatype=int)
# matriz:
# [ [Arreglo(int) [1,2], Arreglo(int) [3]],
#   [Arreglo(int) [4],   Arreglo(int) [5,6]] ]
```

--- 

---

## Ejemplo avanzado: Modelo Dos Vías Clasificación y Multicotomización

### Declaración de variables y modelo

```python
Entero paramGlobal = 4.7;
Arreglo<Flotante> bloques = [5.4, -9.2];
Arreglo<Flotante> tratamientos = [-7.4, 1.2, 0.58];
M2VClasificacion<Flotante> modelo2V = M2VClasificacion<Flotante>(
    paramGlobal, bloques, tratamientos
);
```

### Asignación de valores a la matriz del modelo

```python
Arreglo<Flotante> valores1 = [15.9, -4.0, 66.1];
modelo2V[0][0] = valores1;
modelo2V[0][1] = [-6.1, 3.9];
modelo2V[0][2] = [-1.3, 12.4, 5.8];

modelo2V[1][0] = [23.8];
modelo2V[1][1] = [4.5, 3.6, -0.5];
modelo2V[1][2] = [2.2, -5.6];
```

### Visualización de la matriz de arreglos (modelo2V)

|           | Tratamiento 1 [-7.4] | Tratamiento 2 [1.2] | Tratamiento 3 [0.58] |
|-----------|----------------------|---------------------|----------------------|
| **Bloque 1 [5.4]**  | [15.9, -4.0, 66.1]     | [-6.1, 3.9]         | [-1.3, 12.4, 5.8]      |
| **Bloque 2 [-9.2]** | [23.8]                | [4.5, 3.6, -0.5]    | [2.2, -5.6]            |

---

### Multicotomización

```python
Conjunto<Caracter> categorias = {'a', 'b'};
Multicotomizacion<Flotante> modeloMultiCom = Multicotomizacion<Flotante>(categorias);
modeloMultiCom.añadeRegla(Lambda(X, X < 0.0), 'a');
modeloMultiCom.añadeRegla(Lambda(X, X >= 0.0), 'b');
```

**Reglas:**
- Si el número es negativo → 'a'
- Si el número es positivo o cero → 'b'

---

### Matriz de rachas (cada celda es una cadena de caracteres según la multicotomización)

|           | Tratamiento 1 [-7.4] | Tratamiento 2 [1.2] | Tratamiento 3 [0.58] |
|-----------|----------------------|---------------------|----------------------|
| **Bloque 1 [5.4]**  | "b a b" (15.9, -4.0, 66.1) | "a b" (-6.1, 3.9)      | "a b b" (-1.3, 12.4, 5.8) |
| **Bloque 2 [-9.2]** | "b" (23.8)                | "b b a" (4.5, 3.6, -0.5) | "b a" (2.2, -5.6)         |

### Matriz de rachas (cada celda es una cadena de caracteres según la multicotomización)

|           | Tratamiento 1 [-7.4] | Tratamiento 2 [1.2] | Tratamiento 3 [0.58] |
|-----------|----------------------|---------------------|----------------------|
| **Bloque 1 [5.4]**  | "b a b" | "a b"  | "a b b"  |
| **Bloque 2 [-9.2]** | "b"   | "b b a"  | "b a"  |

**Explicación:**
- Cada celda muestra la cadena resultante de aplicar la multicotomización a la lista de flotantes.
- Por ejemplo, [15.9, -4.0, 66.1] → "b a b" porque 15.9 > 0 → 'b', -4.0 < 0 → 'a', 66.1 > 0 → 'b'.

--- 