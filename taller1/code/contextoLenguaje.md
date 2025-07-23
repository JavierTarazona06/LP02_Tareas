# Estadística de Teoría de Rachas y Pruebas tipo Friedman en el Lenguaje de los Prototipos

Este documento explica las funciones principales de estadística implementadas en los prototipos de lenguaje del repositorio, usando como ejemplo un experimento con distintos tipos de horno que generan pasteles. Se incluyen ejemplos de código inspirados en los archivos de prueba (`prototype1.txt`, `prototype2.txt`).

---

## Contexto: Hornos y Pasteles

Supón que tienes varios **hornos** (bloques) y diferentes **recetas** o **tratamientos**. Cada horno produce varios pasteles, y queremos analizar los resultados para identificar patrones (rachas) y comparar el desempeño de los hornos usando pruebas estadísticas.

---

## 1. Teoría de Rachas

La **teoría de rachas** estudia la secuencia de resultados para identificar patrones consecutivos (rachas) de un mismo tipo. Por ejemplo, podemos clasificar los pasteles como “bien cocidos” (`a`) o “mal cocidos” (`b`) según un umbral de cocción.

### Funciones principales

- **`cadenaMulticotomizada(valores)`**  
  Convierte una lista de valores en una cadena de categorías según reglas (por ejemplo, si el valor es mayor o menor que cierto umbral).

- **`contadoraRachas()`**  
  Devuelve un arreglo que indica, para cada posición, si inicia una nueva racha.

- **`aRachas()`**  
  Devuelve un arreglo con las rachas encontradas (por ejemplo, `["aa", "bb", "a"]`).

- **`numRachas()`**  
  Devuelve el número total de rachas en la cadena.

- **`numRachas(inicio)`**  
  Devuelve el número de rachas a partir de una posición específica.

### Ejemplo aplicado: hornos y cocción de pasteles

Supón que tienes los siguientes resultados de cocción de pasteles en un horno:

```protolang
Arreglo<Flotante> valores = [-1.5, -2.7, 3.0, 4.8, -5.3];
Multicotomizacion<Flotante> modeloMultiCom = Multicotomizacion<Flotante>(categorias);
modeloMultiCom.añadeRegla(X < 0.0, 'a'); // bien cocido
modeloMultiCom.añadeRegla(X >= 0.0, 'b'); // mal cocido

Cadena cadenaMulti = modeloMultiCom.cadenaMulticotomizada(valores);
imprimir(cadenaMulti); // "aabba"

Arreglo<Cadena> rachas = cadenaMulti.aRachas();
imprimir(rachas); // ["aa", "bb", "a"]

Entero numRachas = cadenaMulti.numRachas();
imprimir(numRachas); // 3
```

En este ejemplo:
- Hay dos pasteles bien cocidos seguidos, luego dos mal cocidos, y finalmente uno bien cocido.
- Se identifican 3 rachas.

---

## 2. Prueba tipo Friedman

La **prueba de Friedman** es una prueba estadística no paramétrica para comparar varios tratamientos (recetas) en diferentes bloques (hornos), útil cuando los datos no son necesariamente normales.

### Funciones principales

- **`Matriz<Flotante>`**  
  Representa los resultados de cada horno (bloque) para cada receta (tratamiento).

- **`traeRangos()`**  
  Devuelve una matriz con los rangos asignados a cada resultado dentro de cada bloque.

- **`sumaRangos()`**  
  Suma los rangos por tratamiento para comparar el desempeño de cada receta.

- **`estadFriedman()`**  
  Calcula el estadístico de Friedman para determinar si hay diferencias significativas entre tratamientos.

- **`coefConcordKendall()`**  
  Calcula el coeficiente de concordancia de Kendall para medir el acuerdo entre bloques.

### Ejemplo aplicado: comparación de recetas en hornos

Supón que tienes 3 hornos y 3 recetas, y cada celda es el puntaje de cocción de un pastel:

```protolang
Matriz<Flotante> matrizFried = Matriz<Flotante>(3, 3);
matrizFried[0] = [12.0, 15.0, 10.0];  // Horno 1
matrizFried[1] = [8.0, 9.0, 7.0];     // Horno 2
matrizFried[2] = [20.0, 18.0, 22.0];  // Horno 3

Matriz<Entero> matrizRangos = matrizFried.traeRangos();
imprimir(matrizRangos);
/*
  [[2, 3, 1],
   [2, 3, 1],
   [2, 1, 3]]
*/

Arreglo<Entero> sumaRangos = matrizFried.sumaRangos();
imprimir(sumaRangos); // [6, 7, 5]

Flotante estadFried = matrizFried.estadFriedman();
imprimir(estadFried); // Valor del estadístico de Friedman

Flotante coefKendall = matrizFried.coefConcordKendall();
imprimir(coefKendall); // Valor del coeficiente de concordancia
```

En este ejemplo:
- Se asignan rangos a cada receta dentro de cada horno.
- Se suman los rangos para cada receta.
- Se calcula el estadístico de Friedman y el coeficiente de concordancia de Kendall para evaluar diferencias y acuerdo entre hornos.

---

## Resumen

- **Teoría de rachas**: Permite analizar la secuencia de resultados de los pasteles para ver si hay patrones de hornos que cocinan bien/mal en rachas.
- **Prueba de Friedman**: Permite comparar objetivamente si alguna receta (tratamiento) es mejor que las otras considerando todos los hornos.

Estas funciones y estructuras permiten modelar y analizar experimentos reales de comparación de tratamientos en bloques, como el caso de hornos y pasteles, de manera sencilla y expresiva en el lenguaje de los prototipos. 