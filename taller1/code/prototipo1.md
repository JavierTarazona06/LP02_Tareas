# Explicación detallada de prototype1.txt

Este documento explica, línea por línea y de manera teórica, el archivo `prototype1.txt`, usando el ejemplo de distintos tipos de horno que generan pasteles. Cada instrucción se interpreta en el contexto de un experimento de comparación de hornos y recetas.

---

## Encabezado y función principal

```protolang
// Teoría de Rachas
Func Vacio Principal{
```
- **Comentario**: Indica que el archivo trata sobre teoría de rachas.
- **Func Vacio Principal**: Define la función principal del programa, punto de entrada del experimento.

---

## Definición de categorías y valores

```protolang
Conjunto<Caracter> categorias = {'a', 'b'};
Arreglo<Flotante> valores[5] = [-1.5, -2.7, 3.0, 4.8, -5.3];
```
- **categorias**: Define las posibles categorías de cocción de los pasteles: 'a' (bien cocido), 'b' (mal cocido).
- **valores**: Resultados numéricos de cocción de 5 pasteles en un horno.

---

## Multicotomización: reglas de clasificación

```protolang
Multicotomizacion<Flotante> modeloMultiCom = Multicotomizacion<Flotante>(categorias);
modeloMultiCom.añadeRegla(X < 0.0, 'a');
modeloMultiCom.añadeRegla(X >= 0.0, 'b');
```
- **modeloMultiCom**: Crea un clasificador que asigna cada valor numérico a una categoría.
- **añadeRegla**: Define las reglas: si el valor es menor a 0, el pastel está bien cocido ('a'); si es mayor o igual a 0, está mal cocido ('b').

---

## Aplicación de la multicotomización y análisis de rachas

```protolang
Cadena cadenaMulti = modeloMultiCom.cadenaMulticotomizada(valores);
imprimir(cadenaMulti);
```
- **cadenaMulticotomizada**: Aplica las reglas a los valores y produce una cadena de categorías, por ejemplo "aabba".
- **imprimir**: Muestra la secuencia de cocción de los pasteles.

```protolang
Arreglo<Entero> contadoraRachas = cadenaMulti.contadoraRachas();
imprimir(contadoraRachas);
```
- **contadoraRachas**: Indica en qué posiciones inicia una nueva racha.

```protolang
Arreglo<Cadena> rachas = cadenaMulti.aRachas();
imprimir(rachas);
```
- **aRachas**: Devuelve las rachas encontradas, por ejemplo ["aa", "bb", "a"].

```protolang
Entero numRachas = cadenaMulti.numRachas();
imprimir(numRachas);
```
- **numRachas**: Devuelve el número total de rachas en la secuencia.

```protolang
Entero numRachasParcial = cadenaMulti.numRachas(0);
imprimir(numRachasParcial);
```
- **numRachas(0)**: Devuelve el número de rachas a partir de la posición 0 (toda la cadena).

```protolang
Entero numRachasParcial = cadenaMulti.numRachas(3);
imprimir(numRachasParcial);
```
- **numRachas(3)**: Devuelve el número de rachas a partir de la posición 3 (subsecuencia).

---

## Modelo Dos Vías de Clasificación (bloques y tratamientos)

```protolang
Entero paramGlobal = 4.7;
Arreglo<Flotante> bloques = [5.4, -9.2];
Arreglo<Flotante> tratamientos = [-7.4, 1.2, 0.58];

M2VClasificacion<Flotante> modelo2V = M2VClasificacion<Flotante>(
    paramGlobal, bloques, tratamientos
);
```
- **paramGlobal**: Parámetro global del experimento (puede ser temperatura de referencia).
- **bloques**: Representa los hornos.
- **tratamientos**: Representa las recetas.
- **modelo2V**: Crea una matriz para almacenar los resultados de cada combinación horno-receta.

---

## Asignación de resultados a la matriz

```protolang
Arreglo<Flotante> valores1 = [15.9, -4.0, 66.1];
modelo2V[0][0] = valores1;
modelo2V[0][1] = [-6.1, 3.9];
modelo2V[0][2] = [-1.3, 12.4, 5.8];

modelo2V[1][0] = [23.8];
modelo2V[1][1] = [4.5, 3.6, -0.5];
modelo2V[1][1] = [2.2, -5.6];
```
- Asigna los resultados de cocción de los pasteles a cada celda de la matriz (cada horno con cada receta).

---

## Verificación y visualización de la matriz

```protolang
imprimir(modelo2V.lleno());
```
- Verifica si todas las posiciones de la matriz han sido llenadas con datos.

```protolang
imprimir(modelo2V);
```
- Muestra la matriz completa de resultados.

---

## Consulta de datos y rachas en la matriz

```protolang
imprimir(modelo2V.nDatos(".,."));
imprimir(modelo2V.nDatos("0,2"));
```
- **nDatos**: Devuelve el número de réplicas (pasteles) en toda la matriz o en una celda específica.

```protolang
Conjunto<Flotante> valores = modelo2V.datos(".,.");
imprimir(valores);
Conjunto<Flotante> valores = modelo2V.datos(".,2");
imprimir(valores);
```
- **datos**: Devuelve todos los valores de la matriz o de una columna específica (receta).

---

## Análisis de rachas en la matriz

```protolang
MatrizRachas<Flotante> matrizRachas = 
    modelo2V.matrizRachas(modeloMultiCom);
```
- **matrizRachas**: Convierte los valores numéricos de la matriz en categorías usando las reglas de multicotomización y analiza las rachas en cada celda.

```protolang
Arreglo<Arreglo<Arreglo<Entero>>> arr = matrizRachas.aArreglos();
```
- Convierte la matriz de rachas en un arreglo anidado para su análisis o visualización.

```protolang
Entero matrizRachas.traeRacha("1,1,0");
```
- Devuelve la racha correspondiente a una posición específica (horno, receta, réplica).

---

## Estadísticas de rachas en la matriz

```protolang
Entero sum1 = matrizRachas.sumRachas(".,.,.");
Flotante sum1 = matrizRachas.promRachas(".,.,.");
```
- **sumRachas**: Suma todas las rachas en la matriz.
- **promRachas**: Calcula el promedio de las rachas en la matriz.

---

## Estadístico de Friedman

```protolang
Matriz<Flotante> matrizFried = Matriz<Flotante>(
    bloques.long(), tratamientos.long()
);

Para (Entero i=0; i < bloques.long(); i+=1){
    Para (Entero j=0; j < bloques.long(); j+=1){
        matrizFried[i][j] = matrizRachas.sumRachas(f"{i},{j},.");
    }
}
```
- **matrizFried**: Crea una matriz para almacenar el total de rachas por horno y receta.
- **Para**: Llena la matriz con la suma de rachas de cada combinación horno-receta.

---

Cada línea del prototipo modela un paso del análisis estadístico de los resultados de cocción de pasteles en distintos hornos y recetas, permitiendo desde la clasificación básica hasta el análisis avanzado de patrones y comparación de tratamientos. 