# Explicación detallada de prototype2.txt

Este documento explica, línea por línea y de manera teórica, el archivo `prototype2.txt`, usando el ejemplo de distintos tipos de horno que generan pasteles, en el contexto de pruebas estadísticas tipo Friedman.

---

## Encabezado y función principal

```protolang
// Pruebas tipo Friedman
Func Vacio Principal{
```
- **Comentario**: Indica que el archivo trata sobre pruebas estadísticas tipo Friedman.
- **Func Vacio Principal**: Define la función principal del programa, punto de entrada del experimento.

---

## Definición de parámetros y matriz de resultados

```protolang
Entero nBloques, nTratamientos = 5, 3;
Matriz<Flotante> matrizFried = Matriz<Flotante>(Bloques, nTratamientos);
```
- **nBloques**: Número de hornos (bloques) en el experimento.
- **nTratamientos**: Número de recetas (tratamientos) a comparar.
- **matrizFried**: Matriz para almacenar los resultados de cada combinación horno-receta (cada fila es un horno, cada columna una receta).

---

## Asignación de resultados a la matriz

```protolang
Arreglo<Flotante> arr = [12.0, 15.0, 10.0]; 
matrizFried[0] = arr;
matrizFried[1] = [8.0, 9.0, 7.0];
matrizFried[2] = [20.0, 18.0, 22.0];
matrizFried[3] = [11.0, 14.0, 13.0];
matrizFried[4] = [9.0, 8.0, 12.0];
```
- Asigna los puntajes de cocción de los pasteles producidos por cada horno bajo cada receta. Cada fila representa un horno, cada columna una receta.

---

## Cálculo de rangos y sumas de rangos

```protolang
Matriz<Entero> matrizRangos = matrizFried.traeRangos();
```
- **traeRangos**: Asigna rangos a los resultados de cada horno (fila), ordenando los puntajes de menor a mayor dentro de cada horno.

```protolang
/*
	[[2, 3, 1]
	 [2, 3, 1]
	 [2, 1, 3]
	 [1, 3, 2]
	 [2, 1, 3]]
*/
```
- Ejemplo de salida: cada subarreglo muestra los rangos asignados a las recetas en cada horno.

```protolang
Arreglo<Entero> sumaRangos = matrizFried.sumaRangos();
// [9, 11, 10]
Arreglo<Entero> sumaRangos = matrizFried.sumaRangos(1);
// 11
```
- **sumaRangos**: Suma los rangos de cada receta a través de todos los hornos. Permite comparar el desempeño global de cada receta.
- **sumaRangos(1)**: Suma los rangos solo para la receta 1.

```protolang
Arreglo<Entero> sumaRangos = matrizFried.promRangos(1);
// 11/5
```
- **promRangos(1)**: Calcula el promedio de rangos para la receta 1 (útil para comparar tratamientos en igualdad de condiciones).

---

## Estadísticos de Friedman y otros indicadores

```protolang
Flotante estadFried = matrizFried.estadFriedman();
// 0.4
```
- **estadFriedman**: Calcula el estadístico de Friedman, que permite determinar si existen diferencias significativas entre las recetas considerando todos los hornos.

```protolang
// Grados de libertad
Flotante estadFried = matrizFried.estadFriedmanGL();
```
- **estadFriedmanGL**: Calcula los grados de libertad asociados al estadístico de Friedman.

```protolang
Flotante imanDaven = matrizFried.imanDavenPort();
// Grados de libertad
Flotante imanDaven = matrizFried.imanDavenPortGL();
```
- **imanDavenPort**: Calcula el estadístico de Iman-Davenport-Porter, una corrección para la prueba de Friedman.
- **imanDavenPortGL**: Calcula los grados de libertad para este estadístico.

```protolang
Flotante coefKendall = matrizFried.coefConcordKendall();
Flotante varExp = matrizFried.varianzaExplicada();
Flotante alpha = 0.05;
Flotante varExp = matrizFried.nemenyi(alpha);
```
- **coefConcordKendall**: Calcula el coeficiente de concordancia de Kendall, que mide el acuerdo entre los hornos respecto a las recetas.
- **varianzaExplicada**: Calcula la proporción de la varianza explicada por las diferencias entre tratamientos.
- **nemenyi(alpha)**: Realiza la prueba post-hoc de Nemenyi para comparar pares de recetas si Friedman detecta diferencias significativas (usando un nivel de significancia `alpha`).

---

Cada línea del prototipo modela un paso del análisis estadístico de los resultados de cocción de pasteles en distintos hornos y recetas, permitiendo comparar objetivamente los tratamientos y obtener conclusiones sobre cuál receta es mejor considerando la variabilidad entre hornos. 