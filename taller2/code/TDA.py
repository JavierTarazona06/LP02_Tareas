# Clases agregadas para tiposb contenedores
import numpy as np
from typing import Callable, List, Tuple

def check_datatypeNum(datatype: type) -> None:
    if (datatype != int and datatype != float and datatype != bool and
    datatype != complex):
        raise ValueError("El tipo de dato debe ser int, float, bool o complex")

def check_datatypeA(datatype: type) -> None:
    if (datatype != int and datatype != float and datatype != bool and
    datatype != complex and datatype != Cadena):
        raise ValueError("El tipo de dato debe ser str, int, float, bool, complex o Cadena")

def check_datatypeAPlus(datatype: type) -> None:
    if (datatype != int and datatype != float and datatype != bool and
    datatype != complex and datatype != Cadena and datatype != Arreglo):
        raise ValueError("El tipo de dato debe ser str, int, float, bool, complex, Cadena o Arreglo")

def check_datatype(datatype: type) -> None:
    if (datatype != int and datatype != float and datatype != bool and
    datatype != complex and datatype != Cadena and datatype != Arreglo and datatype != Conjunto
    and datatype != Matriz and datatype != MatrizRachas and datatype != Multicotomizacion
    and datatype != M2VClasificacion and datatype != Diccionario):
        raise ValueError("El tipo de dato debe ser str, int, float, bool, complex, Cadena, Arreglo, Conjunto, Matriz, MatrizRachas, Multicotomizacion, M2VClasificacion o Diccionario")


class Cadena:
    def __init__(self, value: str | None = None):
        if not value:
            value = ""
        self.value = value
    
    def __add__(self, other: "Cadena") -> "Cadena":
        return Cadena(self.value + other.value)
    
    def __len__(self) -> int:
        return len(self.value)
    
    def __repr__(self):
        return f"Cadena({self.value})"
    
    def __iter__(self):
        return iter(self.value)
    
    def __lt__(self, other: "Cadena") -> bool:
        return self.value < other.value
    
    def __le__(self, other: "Cadena") -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: "Cadena") -> bool:
        return self.value > other.value
    
    def __ge__(self, other: "Cadena") -> bool:
        return self.value >= other.value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cadena):
            return NotImplemented
        return self.value == other.value
    
    def __contains__(self, item: str) -> bool:
        return item in self.value
    
    def __str__(self):
        return self.value

    def contadoraRachas(self) -> "Arreglo":
        """
        Devuelve un Arreglo de 1 y 0, donde 1 indica el inicio de una nueva racha y 0 la continuación de la anterior.
        """
        if not self.value:
            return Arreglo(int)
        resultado = [1]
        for i in range(1, len(self.value)):
            resultado.append(1 if self.value[i] != self.value[i-1] else 0)
        arr = Arreglo(int)
        for v in resultado:
            arr.data.append(v)
        return arr

    def aRachas(self) -> "Arreglo":
        """
        Devuelve un Arreglo con las subcadenas de cada racha consecutiva.
        """
        if not self.value:
            return Arreglo(Cadena)
        rachas = []
        actual = self.value[0]
        temp = actual
        for c in self.value[1:]:
            if c == actual:
                temp += c
            else:
                rachas.append(temp)
                actual = c
                temp = c
        rachas.append(temp)
        arr = Arreglo(Cadena)
        for r in rachas:
            r_c = Cadena(r)
            arr.data.append(r_c)
        return arr

    def numRachas(self, pos: int | None = None) -> int:
        """
        Devuelve el número de rachas hasta la posición pos (inclusive),
        o el total si pos es None.
        """
        if not self.value:
            return 0
        count = 1
        last = self.value[0]
        if pos is None:
            pos = len(self.value) - 1
        for i in range(1, pos+1):
            if self.value[i] != last:
                count += 1
                last = self.value[i]
        return count

    def promRachas(self, pos: int | None = None) -> float:
        """
        Devuelve el promedio de rachas a la posición pos (inclusive),
        o el de toda la cadena si pos es None.
        """
        if not self.value:
            return 0.0
        if pos is None:
            pos = len(self.value) - 1

        valores = []
        for i in range(pos+1):
            valores.append(self.numRachas(i))
        promedio = sum(valores) / len(valores)

        return promedio

    def toArregloChar(self) -> "Arreglo":
        """
        Convierte la cadena a un Arreglo con datatype Cadena. Separa los caracteres de la cadena.
        """
        arr: Arreglo = Arreglo(Cadena)
        for char in self.value:
            arr.pushback(Cadena(char))
        return arr

    def __getitem__(self, index: int) -> "Cadena":
        """
        Permite acceso como cadena[index]. Devuelve una Cadena con el carácter en esa posición.
        """
        if index < 0 or index >= len(self.value):
            raise IndexError("Índice fuera de rango")
        return Cadena(self.value[index])

    def __setitem__(self, index: int, value: "Cadena") -> None:
        """
        Permite asignación como cadena[index] = value. Modifica la cadena original.
        """
        if index < 0 or index >= len(self.value):
            raise IndexError("Índice fuera de rango")
        if not isinstance(value, Cadena):
            raise ValueError("value debe ser una Cadena")
        self.value = self.value[:index] + value.value + self.value[index+1:]

class Conjunto:
    def __init__(self, datatype: type) -> None:
        check_datatype(datatype)
        self.datatype: type = datatype
        self.data: list = []
    
    def add(self, value: object) -> None:
        if not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype}")
        if value not in self.data:
            self.data.append(value)
    
    def remove(self, value: object) -> None:
        self.data.remove(value)

    def __add__(self, other: "Conjunto") -> "Conjunto":
        if not isinstance(other, Conjunto):
            return NotImplemented
        if self.datatype != other.datatype:
            raise TypeError("Ambos conjuntos deben tener el mismo tipo de dato")
        nuevo = Conjunto(self.datatype)
        nuevo.data = list(set(self.data) | set(other.data))
        return nuevo

    def __sub__(self, other: "Conjunto") -> "Conjunto":
        if not isinstance(other, Conjunto):
            return NotImplemented
        if self.datatype != other.datatype:
            raise TypeError("Ambos conjuntos deben tener el mismo tipo de dato")
        nuevo = Conjunto(self.datatype)
        nuevo.data = list(set(self.data) - set(other.data))
        return nuevo

    def __lt__(self, other: "Conjunto") -> bool:
        if not isinstance(other, Conjunto):
            return NotImplemented
        return len(self.data) < len(other.data)

    def __le__(self, other: "Conjunto") -> bool:
        if not isinstance(other, Conjunto):
            return NotImplemented
        return len(self.data) <= len(other.data)

    def __gt__(self, other: "Conjunto") -> bool:
        if not isinstance(other, Conjunto):
            return NotImplemented
        return len(self.data) > len(other.data)

    def __ge__(self, other: "Conjunto") -> bool:
        if not isinstance(other, Conjunto):
            return NotImplemented
        return len(self.data) >= len(other.data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Conjunto):
            return NotImplemented
        return set(self.data) == set(other.data)

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item) -> bool:
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"Conjunto({self.data})"

    def __str__(self):
        return str(self.data)

class Arreglo:
    def __init__(self, datatype: type):
        check_datatype(datatype)
        self.datatype = datatype
        self.data = []

    def pushback(self, value) -> None:
        """
        Añade un elemento al final del arreglo.
        """
        if value is not None and not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype} o None")
        self.data.append(value)

    def pushfront(self, value) -> None:
        """
        Añade un elemento al inicio del arreglo.
        """
        if value is not None and not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype} o None")
        self.data.insert(0, value)

    def back(self):
        """
        Devuelve el último elemento del arreglo.
        """
        if not self.data:
            raise IndexError("El arreglo está vacío")
        return self.data[-1]

    def front(self):
        """
        Devuelve el primer elemento del arreglo.
        """
        if not self.data:
            raise IndexError("El arreglo está vacío")
        return self.data[0]

    def popback(self):
        """
        Elimina y devuelve el último elemento del arreglo.
        """
        if not self.data:
            raise IndexError("El arreglo está vacío")
        return self.data.pop()

    def popfront(self):
        """
        Elimina y devuelve el primer elemento del arreglo.
        """
        if not self.data:
            raise IndexError("El arreglo está vacío")
        return self.data.pop(0)

    def insert(self, position: int, value) -> None:
        """
        Inserta un elemento en la posición especificada.
        """
        if value is not None and not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype} o None")
        if position < 0 or position > len(self.data):
            raise IndexError("Posición fuera de rango")
        self.data.insert(position, value)

    def delete(self, position: int) -> None:
        """
        Elimina el elemento en la posición especificada.
        """
        if position < 0 or position >= len(self.data):
            raise IndexError("Posición fuera de rango")
        del self.data[position]

    def __add__(self, other: "Arreglo") -> "Arreglo":
        if not isinstance(other, Arreglo):
            return NotImplemented
        if self.datatype != other.datatype:
            raise TypeError("Ambos arreglos deben tener el mismo tipo de dato")
        nuevo = Arreglo(self.datatype)
        nuevo.data = self.data + other.data
        return nuevo

    def __sub__(self, other: "Arreglo") -> "Arreglo":
        if not isinstance(other, Arreglo):
            return NotImplemented
        if self.datatype != other.datatype:
            raise TypeError("Ambos arreglos deben tener el mismo tipo de dato")
        nuevo = Arreglo(self.datatype)
        nuevo.data = [x for x in self.data if x not in other.data]
        return nuevo

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        if value is not None and not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype} o None")
        self.data[idx] = value

    def __contains__(self, item) -> bool:
        return item in self.data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Arreglo):
            return NotImplemented
        return self.data == other.data

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"Arreglo({self.data})"

    def __str__(self):
        return str(self.data)

class Diccionario:
    def __init__(self, key_datatype: type, value_datatype: type):
        check_datatypeA(key_datatype)
        check_datatypeA(value_datatype)
        self.key_datatype = key_datatype
        self.value_datatype = value_datatype
        self.data = {}

    def __setitem__(self, key, value):
        """
        Asigna un valor a una clave: diccionario[clave] = valor
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        if not isinstance(value, self.value_datatype):
            raise ValueError(f"El valor debe ser de tipo {self.value_datatype}")
        self.data[key] = value

    def __getitem__(self, key):
        """
        Obtiene un valor por su clave: valor = diccionario[clave]
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        if key not in self.data:
            raise KeyError(f"La clave {key} no existe en el diccionario")
        return self.data[key]

    def __delitem__(self, key):
        """
        Elimina un elemento por su clave: del diccionario[clave]
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        if key not in self.data:
            raise KeyError(f"La clave {key} no existe en el diccionario")
        del self.data[key]

    def __contains__(self, key) -> bool:
        """
        Verifica si una clave existe en el diccionario: clave in diccionario
        """
        return key in self.data

    def __len__(self) -> int:
        """
        Devuelve el número de elementos en el diccionario: len(diccionario)
        """
        return len(self.data)

    def __iter__(self):
        """
        Permite iterar sobre las claves del diccionario
        """
        return iter(self.data)

    def keys(self):
        """
        Devuelve una vista de las claves del diccionario
        """
        return self.data.keys()

    def values(self):
        """
        Devuelve una vista de los valores del diccionario
        """
        return self.data.values()

    def items(self):
        """
        Devuelve una vista de los pares (clave, valor) del diccionario
        """
        return self.data.items()

    def get(self, key, default=None):
        """
        Obtiene un valor por su clave, devolviendo un valor por defecto si no existe
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        return self.data.get(key, default)

    def pop(self, key, default=None):
        """
        Elimina y devuelve el valor asociado a una clave
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        
        if key in self.data:
            return self.data.pop(key)
        elif default is not None:
            return default
        else:
            raise KeyError(f"La clave {key} no existe en el diccionario")

    def clear(self):
        """
        Elimina todos los elementos del diccionario
        """
        self.data.clear()

    def update(self, other):
        """
        Actualiza el diccionario con elementos de otro diccionario o iterable de pares
        """
        if isinstance(other, Diccionario):
            if self.key_datatype != other.key_datatype:
                raise TypeError("Los diccionarios deben tener el mismo tipo de clave")
            if self.value_datatype != other.value_datatype:
                raise TypeError("Los diccionarios deben tener el mismo tipo de valor")
            for key, value in other.items():
                self[key] = value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            # Asumir que es un iterable de pares (clave, valor)
            for key, value in other:
                self[key] = value

    def setdefault(self, key, default=None):
        """
        Obtiene el valor de una clave, o la establece con un valor por defecto si no existe
        """
        if not isinstance(key, self.key_datatype):
            raise ValueError(f"La clave debe ser de tipo {self.key_datatype}")
        
        if key in self.data:
            return self.data[key]
        else:
            if default is not None and not isinstance(default, self.value_datatype):
                raise ValueError(f"El valor por defecto debe ser de tipo {self.value_datatype}")
            self.data[key] = default
            return default

    def copy(self) -> "Diccionario":
        """
        Crea una copia superficial del diccionario
        """
        nuevo = Diccionario(self.key_datatype, self.value_datatype)
        nuevo.data = self.data.copy()
        return nuevo

    def __eq__(self, other) -> bool:
        """
        Compara dos diccionarios por igualdad
        """
        if not isinstance(other, Diccionario):
            return NotImplemented
        return (self.key_datatype == other.key_datatype and 
                self.value_datatype == other.value_datatype and 
                self.data == other.data)

    def __repr__(self):
        """
        Representación string para debugging
        """
        return f"Diccionario(key_type={self.key_datatype.__name__}, value_type={self.value_datatype.__name__}, data={self.data})"

    def __str__(self):
        """
        Representación string legible
        """
        return str(self.data)

class Matriz:
    def __init__(self, filas: int, columnas: int, datatype: type):
        check_datatypeAPlus(datatype)
        self.filas = filas
        self.columnas = columnas
        self.datatype = datatype
        self.data = Arreglo(Arreglo)
        for i in range(filas):
            fila = Arreglo(self.datatype)
            for j in range(columnas):
                fila.pushback(None)  # Inicializar con None
            self.data.pushback(fila)

    def modificar(self, fila: int, columna: int, valor) -> None:
        """
        Modifica el elemento en la posición [fila][columna] con el valor dado.
        """
        if not (0 <= fila < self.filas):
            raise IndexError("Índice de fila fuera de rango")
        if not (0 <= columna < self.columnas):
            raise IndexError("Índice de columna fuera de rango")
        if not isinstance(valor, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype}")
        self.data[fila][columna] = valor

    def __getitem__(self, fila: int):
        """
        Permite acceso como matriz[fila][columna]
        """
        if not (0 <= fila < self.filas):
            raise IndexError("Índice de fila fuera de rango")
        return self.data[fila]

    def __setitem__(self, fila: int, valores):
        """
        Permite asignar una fila completa como matriz[fila] = [valores]
        """
        if not (0 <= fila < self.filas):
            raise IndexError("Índice de fila fuera de rango")
        if len(valores) != self.columnas:
            raise ValueError(f"La fila debe tener {self.columnas} elementos")
        for val in valores:
            if not isinstance(val, self.datatype):
                raise ValueError(f"Todos los valores deben ser de tipo {self.datatype}")
        self.data[fila] = list(valores)

    def __add__(self, other: "Matriz") -> "Matriz":
        """
        Suma de matrices. Ambas matrices deben tener las mismas dimensiones.
        """
        if not isinstance(other, Matriz):
            return NotImplemented
        if self.filas != other.filas or self.columnas != other.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones para sumarse")
        if self.datatype != other.datatype:
            raise TypeError("Ambas matrices deben tener el mismo tipo de dato")
        
        resultado = Matriz(self.filas, self.columnas, self.datatype)
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.data[i][j] is None or other.data[i][j] is None:
                    raise ValueError("No se pueden sumar matrices con elementos None")
                resultado.data[i][j] = self.data[i][j] + other.data[i][j]
        return resultado

    def __sub__(self, other: "Matriz") -> "Matriz":
        """
        Resta de matrices. Ambas matrices deben tener las mismas dimensiones.
        """
        if not isinstance(other, Matriz):
            return NotImplemented
        if self.filas != other.filas or self.columnas != other.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones para restarse")
        if self.datatype != other.datatype:
            raise TypeError("Ambas matrices deben tener el mismo tipo de dato")
        
        resultado = Matriz(self.filas, self.columnas, self.datatype)
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.data[i][j] is None or other.data[i][j] is None:
                    raise ValueError("No se pueden restar matrices con elementos None")
                resultado.data[i][j] = self.data[i][j] - other.data[i][j]
        return resultado

    def __mul__(self, escalar) -> "Matriz":
        """
        Multiplicación por escalar. El escalar debe ser numérico.
        """
        if not isinstance(escalar, (int, float, complex)):
            raise TypeError("El escalar debe ser int, float o complex")
        
        resultado = Matriz(self.filas, self.columnas, self.datatype)
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.data[i][j] is None:
                    raise ValueError("No se puede multiplicar una matriz con elementos None")
                resultado.data[i][j] = self.datatype(self.data[i][j] * escalar)
        return resultado

    def __matmul__(self, other: "Matriz") -> "Matriz":
        """
        Multiplicación de matrices usando el operador @.
        El número de columnas de la primera matriz debe ser igual al número de filas de la segunda.
        """
        if not isinstance(other, Matriz):
            return NotImplemented
        if self.columnas != other.filas:
            raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda")
        if self.datatype != other.datatype:
            raise TypeError("Ambas matrices deben tener el mismo tipo de dato")
        
        resultado = Matriz(self.filas, other.columnas, self.datatype)
        for i in range(self.filas):
            for j in range(other.columnas):
                suma = self.datatype(0)
                for k in range(self.columnas):
                    if self.data[i][k] is None or other.data[k][j] is None:
                        raise ValueError("No se pueden multiplicar matrices con elementos None")
                    suma += self.data[i][k] * other.data[k][j]
                resultado.data[i][j] = self.datatype(suma)
        return resultado

    def __truediv__(self, escalar) -> "Matriz":
        """
        División por escalar (equivale a multiplicar por el inverso del escalar).
        """
        if not isinstance(escalar, (int, float, complex)):
            raise TypeError("El escalar debe ser int, float o complex")
        if escalar == 0:
            raise ZeroDivisionError("No se puede dividir por cero")
        
        return self.__mul__(1 / escalar)

    def determinante(self) -> float:
        """
        Calcula el determinante de la matriz. Solo aplicable a matrices cuadradas.
        """
        if self.filas != self.columnas:
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas")
        
        # Verificar que no hay elementos None
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.data[i][j] is None:
                    raise ValueError("No se puede calcular el determinante de una matriz con elementos None")
        
        # Convertir la matriz a float para los cálculos
        matriz_float = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(float(self.data[i][j]))
            matriz_float.append(fila)
        
        return self._determinante_recursivo(matriz_float)

    def _determinante_recursivo(self, matriz: list) -> float:
        """
        Calcula el determinante de forma recursiva usando expansión por cofactores.
        """
        n = len(matriz)
        
        # Caso base: matriz 1x1
        if n == 1:
            return matriz[0][0]
        
        # Caso base: matriz 2x2
        if n == 2:
            return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        
        # Expansión por la primera fila
        det = 0
        for j in range(n):
            # Crear submatriz eliminando fila 0 y columna j
            submatriz = []
            for i in range(1, n):
                fila = []
                for k in range(n):
                    if k != j:
                        fila.append(matriz[i][k])
                submatriz.append(fila)
            
            # Calcular cofactor
            cofactor = ((-1) ** j) * matriz[0][j] * self._determinante_recursivo(submatriz)
            det += cofactor
        
        return det

    def determinante_rapido(self) -> float:
        """
        Calcula el determinante de la matriz usando numpy.linalg.det para mayor eficiencia.
        Solo aplicable a matrices cuadradas.
        """
        if self.filas != self.columnas:
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas")
        
        # Verificar que no hay elementos None
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.data[i][j] is None:
                    raise ValueError("No se puede calcular el determinante de una matriz con elementos None")
        
        # Convertir la matriz a array de numpy
        try:
            matriz_numpy = np.array(self.data, dtype=float)
            return float(np.linalg.det(matriz_numpy))
        except ImportError:
            # Si numpy no está disponible, usar el método recursivo
            raise ImportError("numpy no está disponible. Use el método determinante() en su lugar.")

    def __repr__(self):
        """
        Representación string para debugging de la matriz
        """
        return f"Matriz(filas={self.filas}, columnas={self.columnas}, datatype={self.datatype.__name__}, data={self.data})"

    def __str__(self):
        """
        Representación string legible de la matriz en formato tabular
        """
        if not self.data or not self.data[0]:
            return "Matriz vacía"
        
        # Calcular el ancho máximo necesario para cada columna
        anchos_columnas = []
        for j in range(self.columnas):
            ancho_max = 0
            for i in range(self.filas):
                elemento = self.data[i][j]
                str_elemento = str(elemento) if elemento is not None else "None"
                ancho_max = max(ancho_max, len(str_elemento))
            anchos_columnas.append(ancho_max)
        
        # Construir la representación string
        lineas = []
        for i in range(self.filas):
            elementos_fila = []
            for j in range(self.columnas):
                elemento = self.data[i][j]
                str_elemento = str(elemento) if elemento is not None else "None"
                # Justificar a la derecha con el ancho calculado
                str_elemento_justificado = str_elemento.rjust(anchos_columnas[j])
                elementos_fila.append(str_elemento_justificado)
            linea = "[" + " ".join(elementos_fila) + "]"
            lineas.append(linea)
        
        return "\n".join(lineas)

    def __iter__(self):
        """
        Permite iterar sobre las filas de la matriz.
        """
        return iter(self.data)

    def __len__(self) -> int:
        """
        Devuelve el número de filas de la matriz.
        """
        return self.filas

    def getRangos(self) -> "Matriz":
        """
        Devuelve una nueva Matriz con datatype int donde cada fila contiene 
        los rangos (orden) de los elementos de la fila original, empezando desde 1.
        
        El rango 1 corresponde al elemento más pequeño, 2 al siguiente, etc.
        
        Ejemplo:
        Fila original: [12, 15, 10] 
        Fila de rangos: [2, 3, 1]   (10 es rango 1, 12 es rango 2, 15 es rango 3)
        
        Returns:
            Matriz: Nueva matriz de enteros con los rangos por fila
        """
        matriz_rangos = Matriz(self.filas, self.columnas, int)
        
        for i in range(self.filas):
            # Obtener la fila actual
            fila_actual = []
            for j in range(self.columnas):
                fila_actual.append(self.data[i][j])
            
            # Calcular rangos para esta fila
            rangos_fila = self._calcular_rangos_fila(fila_actual)
            
            # Asignar rangos a la matriz resultado
            for j in range(self.columnas):
                matriz_rangos.modificar(i, j, rangos_fila[j])
        
        return matriz_rangos

    def _calcular_rangos_fila(self, fila: list) -> list:
        """
        Calcula los rangos de los elementos en una fila.
        
        Args:
            fila: Lista de elementos de la fila
            
        Returns:
            list: Lista de rangos correspondientes a cada posición
        """
        # Crear lista de (valor, índice_original) excluyendo None
        valores_con_indices = []
        for j, valor in enumerate(fila):
            if valor is not None:
                valores_con_indices.append((valor, j))
        
        # Ordenar por valor (ascendente)
        valores_con_indices.sort(key=lambda x: x[0])
        
        # Inicializar rangos con 0 (para posiciones None)
        rangos = [0] * len(fila)
        
        # Asignar rangos
        for rango, (valor, indice_original) in enumerate(valores_con_indices, 1):
            rangos[indice_original] = rango
        
        return rangos

    def sumaRangos(self, columna: int | None = None):
        """
        Calcula la suma de valores por columna de la matriz.
        
        Args:
            columna: Si es None, devuelve un Arreglo con las sumas de todas las columnas.
                     Si es un entero, devuelve solo la suma de esa columna específica.
        
        Returns:
            Arreglo con las sumas por columna, o un valor individual si se especifica columna
        """
        matrizRangos: Matriz = self.getRangos()

        # Crear arreglo para almacenar las sumas por columna
        sumas = Arreglo(matrizRangos.datatype)
        
        # Calcular suma por cada columna
        for j in range(self.columnas):
            suma_columna = matrizRangos.datatype(0)  # Inicializar con cero del tipo correcto
            for i in range(self.filas):
                valor = matrizRangos[i][j]
                if valor is not None:
                    suma_columna += valor
            sumas.pushback(suma_columna)
        
        # Si se especifica una columna, devolver solo ese valor
        if columna is not None:
            if not (0 <= columna < self.columnas):
                raise IndexError(f"Índice de columna {columna} fuera de rango (0-{self.columnas-1})")
            return sumas[columna]
        
        # Si no se especifica columna, devolver todo el arreglo
        return sumas

    def promRangos(self, columna: int | None = None):
        """
        Calcula el promedio de rangos por columna de la matriz.
        
        Args:
            columna: Si es None, devuelve un Arreglo con los promedios de todas las columnas.
                     Si es un entero, devuelve solo el promedio de esa columna específica.
        
        Returns:
            Arreglo con los promedios por columna, o un valor individual si se especifica columna
        """
        # Obtener matriz de rangos
        matrizRangos = self.getRangos()
        
        # Crear arreglo para almacenar los promedios por columna
        promedios = Arreglo(float)
        
        # Calcular promedio por cada columna
        for j in range(self.columnas):
            suma_columna = 0
            count_valores = 0
            
            # Sumar valores no-None y contar elementos válidos
            for i in range(self.filas):
                valor = matrizRangos[i][j]
                if valor is not None and valor != 0:  # Excluir None (rango 0)
                    suma_columna += valor
                    count_valores += 1
            
            # Calcular promedio
            if count_valores > 0:
                promedio = suma_columna / count_valores
            else:
                promedio = 0.0
            
            promedios.pushback(promedio)
        
        # Si se especifica una columna, devolver solo ese valor
        if columna is not None:
            if not (0 <= columna < self.columnas):
                raise IndexError(f"Índice de columna {columna} fuera de rango (0-{self.columnas-1})")
            return promedios[columna]
        
        # Si no se especifica columna, devolver todo el arreglo
        return promedios

    def estadFriedman(self) -> float:
        """
        Calcula el estadístico de Friedman para la matriz de datos.
        
        La prueba de Friedman es una alternativa no paramétrica al ANOVA de medidas repetidas.
        Se basa en rangos y evalúa si hay diferencias significativas entre tratamientos.
        
        Fórmula: χ² = (12 / (n * k * (k + 1))) * Σ(Rj²) - 3 * n * (k + 1)
        
        Donde:
        - n = número de bloques (filas)
        - k = número de tratamientos (columnas)
        - Rj = suma de rangos para el tratamiento j
        
        Returns:
            float: Valor del estadístico de Friedman (distribución Chi-cuadrado)
        """
        # Verificar que la matriz tenga datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para la prueba de Friedman")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para la prueba de Friedman")
        
        # Parámetros de la prueba
        n = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        # Obtener las sumas de rangos por tratamiento
        sumas_rangos = self.sumaRangos()
        
        # Verificar que no hay valores None en las sumas
        for i, suma in enumerate(sumas_rangos):
            if suma is None:
                raise ValueError(f"La suma de rangos para el tratamiento {i} es None")
        
        # Calcular Σ(Rj²) - suma de cuadrados de las sumas de rangos
        suma_cuadrados_rangos = 0
        for suma in sumas_rangos:
            suma_cuadrados_rangos += suma * suma
        
        # Aplicar la fórmula del estadístico de Friedman
        # χ² = (12 / (n * k * (k + 1))) * Σ(Rj²) - 3 * n * (k + 1)
        termino_1 = 12.0 / (n * k * (k + 1))
        termino_2 = suma_cuadrados_rangos
        termino_3 = 3 * n * (k + 1)
        
        estadistico = termino_1 * termino_2 - termino_3
        
        return estadistico

    def estadFriedmanGL(self) -> int:
        """
        Calcula los grados de libertad para la prueba de Friedman.
        
        Los grados de libertad en la prueba de Friedman se calculan como:
        GL = k - 1
        
        Donde:
        - k = número de tratamientos (columnas)
        
        Returns:
            int: Grados de libertad para la distribución Chi-cuadrado
        """
        # Verificar que la matriz tenga al menos 2 tratamientos
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para calcular grados de libertad")
        
        # Grados de libertad = número de tratamientos - 1
        grados_libertad = self.columnas - 1
        
        return grados_libertad

    def estadImanDavenport(self) -> float:
        """
        Calcula el estadístico de Iman-Davenport, que es una mejora de la prueba de Friedman.
        
        La prueba de Iman-Davenport proporciona una mejor aproximación estadística que Friedman,
        especialmente para muestras pequeñas, usando la distribución F en lugar de Chi-cuadrado.
        
        Fórmula: FF = [(N-1) * χ²] / [N*(k-1) - χ²]
        
        Donde:
        - N = número de bloques (filas)
        - k = número de tratamientos (columnas)  
        - χ² = estadístico de Friedman
        
        Returns:
            float: Valor del estadístico de Iman-Davenport (distribución F)
        """
        # Verificar que la matriz tenga datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para la prueba de Iman-Davenport")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para la prueba de Iman-Davenport")
        
        # Parámetros
        N = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        # Calcular estadístico de Friedman
        chi_cuadrado = self.estadFriedman()
        
        # Verificar que el denominador no sea cero
        denominador = N * (k - 1) - chi_cuadrado
        if abs(denominador) < 1e-10:  # Prácticamente cero
            raise ValueError("El denominador de Iman-Davenport es cero o muy cercano a cero")
        
        # Aplicar fórmula de Iman-Davenport
        # FF = [(N-1) * χ²] / [N*(k-1) - χ²]
        numerador = (N - 1) * chi_cuadrado
        estadistico_f = numerador / denominador
        
        return estadistico_f

    def estadImanDavenportGL(self) -> tuple[int, int]:
        """
        Calcula los grados de libertad para la prueba de Iman-Davenport.
        
        Los grados de libertad para la distribución F son:
        - gl1 (numerador) = k - 1
        - gl2 (denominador) = (k - 1) * (N - 1)
        
        Returns:
            tuple[int, int]: (gl1, gl2) grados de libertad para la distribución F
        """
        # Verificar que la matriz tenga datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para calcular grados de libertad")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para calcular grados de libertad")
        
        N = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        gl1 = k - 1                    # grados de libertad del numerador
        gl2 = (k - 1) * (N - 1)       # grados de libertad del denominador
        
        return (gl1, gl2)

    def pruebaImanDavenport(self) -> "Diccionario":
        """
        Realiza la prueba completa de Iman-Davenport y devuelve un diccionario con los resultados.
        
        Returns:
            Diccionario(str, float): Contiene:
            - "estadistico_f": Valor del estadístico de Iman-Davenport
            - "estadistico_friedman": Valor del estadístico de Friedman original
            - "gl1": Grados de libertad del numerador
            - "gl2": Grados de libertad del denominador  
            - "bloques": Número de bloques
            - "tratamientos": Número de tratamientos
            - "suma_rangos_str": Representación string de sumas de rangos
            - "prom_rangos_str": Representación string de promedios de rangos
        """
        # Calcular estadísticos
        estadistico_f = self.estadImanDavenport()
        estadistico_friedman = self.estadFriedman()
        
        # Calcular grados de libertad
        gl1, gl2 = self.estadImanDavenportGL()
        
        # Obtener sumas y promedios de rangos
        sumas_rangos = self.sumaRangos()
        promedios_rangos = self.promRangos()
        
        # Crear diccionario con resultados
        resultados = Diccionario(str, float)
        resultados["estadistico_f"] = estadistico_f
        resultados["estadistico_friedman"] = estadistico_friedman
        resultados["gl1"] = float(gl1)
        resultados["gl2"] = float(gl2)
        resultados["bloques"] = float(self.filas)
        resultados["tratamientos"] = float(self.columnas)
        # Para los arreglos, convertimos a string para almacenar
        resultados["suma_rangos_str"] = str(sumas_rangos)
        resultados["prom_rangos_str"] = str(promedios_rangos)
        
        return resultados

    def coefConcordKendall(self) -> float:
        """
        Calcula el Coeficiente de Concordancia de Kendall (W).
        
        El Coeficiente de Concordancia de Kendall mide el grado de acuerdo entre 
        múltiples evaluadores (bloques) en el ranking de múltiples objetos (tratamientos).
        
        Fórmula: W = χ² / [n * (k - 1)]
        
        Donde:
        - χ² = estadístico de Friedman
        - n = número de bloques (filas)
        - k = número de tratamientos (columnas)
        
        El valor de W varía entre 0 y 1:
        - W = 0: No hay concordancia entre evaluadores
        - W = 1: Concordancia perfecta entre evaluadores
        
        Returns:
            float: Coeficiente de Concordancia de Kendall (0 ≤ W ≤ 1)
        """
        # Verificar que la matriz tenga datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para calcular el coeficiente de Kendall")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para calcular el coeficiente de Kendall")
        
        # Parámetros
        n = self.filas      # número de bloques (evaluadores)
        k = self.columnas   # número de tratamientos (objetos)
        
        # Calcular estadístico de Friedman
        chi_cuadrado = self.estadFriedman()
        
        # Calcular coeficiente de Kendall usando la relación con Friedman
        # W = χ² / [n * (k - 1)]
        denominador = n * (k - 1)
        w_kendall = chi_cuadrado / denominador
        
        # Asegurar que W esté en el rango [0, 1]
        if w_kendall < 0:
            w_kendall = 0.0
        elif w_kendall > 1:
            w_kendall = 1.0
            
        return w_kendall

    def interpretacionKendall(self, w: float) -> str:
        """
        Proporciona una interpretación del valor del Coeficiente de Kendall.
        
        Args:
            w: Valor del Coeficiente de Concordancia de Kendall
            
        Returns:
            str: Interpretación del nivel de concordancia
        """
        if w < 0.1:
            return "Concordancia muy débil"
        elif w < 0.3:
            return "Concordancia débil"
        elif w < 0.5:
            return "Concordancia moderada"
        elif w < 0.7:
            return "Concordancia fuerte"
        elif w < 0.9:
            return "Concordancia muy fuerte"
        else:
            return "Concordancia casi perfecta"

    def analisisKendall(self) -> "Diccionario":
        """
        Realiza el análisis completo del Coeficiente de Concordancia de Kendall.
        
        Returns:
            Diccionario(str, float): Contiene:
            - "coeficiente_w": Valor del coeficiente de Kendall
            - "estadistico_friedman": Estadístico de Friedman usado en el cálculo
            - "bloques": Número de bloques (evaluadores)
            - "tratamientos": Número de tratamientos (objetos)
            - "interpretacion_num": Código numérico de interpretación (0-5)
            - "suma_rangos_str": Representación string de sumas de rangos
            - "prom_rangos_str": Representación string de promedios de rangos
        """
        # Calcular coeficiente de Kendall
        w_kendall = self.coefConcordKendall()
        
        # Obtener estadístico de Friedman
        friedman = self.estadFriedman()
        
        # Obtener interpretación numérica
        if w_kendall < 0.1:
            interpretacion_num = 0  # Muy débil
        elif w_kendall < 0.3:
            interpretacion_num = 1  # Débil
        elif w_kendall < 0.5:
            interpretacion_num = 2  # Moderada
        elif w_kendall < 0.7:
            interpretacion_num = 3  # Fuerte
        elif w_kendall < 0.9:
            interpretacion_num = 4  # Muy fuerte
        else:
            interpretacion_num = 5  # Casi perfecta
        
        # Obtener sumas y promedios de rangos
        sumas_rangos = self.sumaRangos()
        promedios_rangos = self.promRangos()
        
        # Crear diccionario con resultados
        resultados = Diccionario(str, float)
        resultados["coeficiente_w"] = w_kendall
        resultados["estadistico_friedman"] = friedman
        resultados["bloques"] = float(self.filas)
        resultados["tratamientos"] = float(self.columnas)
        resultados["interpretacion_num"] = float(interpretacion_num)
        # Para los arreglos, convertimos a string para almacenar
        resultados["suma_rangos_str"] = str(sumas_rangos)
        resultados["prom_rangos_str"] = str(promedios_rangos)
        
        return resultados

    def pruebaFriedman(self) -> "Diccionario":
        """
        Realiza la prueba completa de Friedman y devuelve un diccionario con los resultados.
        
        Returns:
            Diccionario(str, float): Contiene:
            - "estadistico": Valor del estadístico de Friedman
            - "grados_libertad": Grados de libertad (k-1)
            - "bloques": Número de bloques
            - "tratamientos": Número de tratamientos
            - "suma_rangos_str": Representación string de sumas de rangos
            - "prom_rangos_str": Representación string de promedios de rangos
        """
        # Calcular estadístico
        estadistico = self.estadFriedman()
        
        # Calcular grados de libertad
        grados_libertad = self.estadFriedmanGL()
        
        # Obtener sumas y promedios de rangos
        sumas_rangos = self.sumaRangos()
        promedios_rangos = self.promRangos()
        
        # Crear diccionario con resultados usando float como tipo general
        resultados = Diccionario(str, float)
        resultados["estadistico"] = estadistico
        resultados["grados_libertad"] = float(grados_libertad)
        resultados["bloques"] = float(self.filas)
        resultados["tratamientos"] = float(self.columnas)
        # Para los arreglos, convertimos a string para almacenar
        resultados["suma_rangos_str"] = str(sumas_rangos)
        resultados["prom_rangos_str"] = str(promedios_rangos)
        
        return resultados

    def varianzaExplicada(self) -> float:
        """
        Calcula la proporción de varianza explicada por los tratamientos en el análisis de rangos.
        
        La varianza explicada indica qué proporción de la variabilidad total en los rangos
        se debe a las diferencias sistemáticas entre tratamientos (no al azar).
        
        En el contexto de rangos, la varianza explicada es equivalente al Coeficiente 
        de Concordancia de Kendall (W).
        
        Fórmula alternativa: VE = SS_tratamientos / SS_total
        
        Donde:
        - SS_tratamientos = suma de cuadrados entre tratamientos
        - SS_total = suma de cuadrados total (varianza máxima posible)
        
        Returns:
            float: Proporción de varianza explicada (0 ≤ VE ≤ 1)
        """
        # Verificar que la matriz tenga datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para calcular varianza explicada")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para calcular varianza explicada")
        
        # Para rangos, la varianza explicada es igual al coeficiente de Kendall
        return self.coefConcordKendall()

    def _calcularSumaCuadradosTratamientos(self) -> float:
        """
        Calcula la suma de cuadrados entre tratamientos (SS_between).
        
        Formula: SS_tratamientos = n * Σ(R̄ⱼ - R̄..)²
        
        Returns:
            float: Suma de cuadrados entre tratamientos
        """
        n = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        # Obtener las sumas de rangos por tratamiento
        sumas_rangos = self.sumaRangos()
        
        # Calcular el rango promedio general
        # R̄.. = (suma total de rangos) / (n * k)
        # En una matriz de rangos completa: suma total = n * k * (k + 1) / 2
        rango_promedio_general = (k + 1) / 2.0
        
        # Calcular SS_tratamientos
        ss_tratamientos = 0.0
        for suma_rango in sumas_rangos:
            rango_promedio_tratamiento = suma_rango / n  # R̄ⱼ
            diferencia = rango_promedio_tratamiento - rango_promedio_general
            ss_tratamientos += diferencia * diferencia
        
        ss_tratamientos *= n  # Multiplicar por n
        
        return ss_tratamientos

    def _calcularSumaCuadradosTotal(self) -> float:
        """
        Calcula la suma de cuadrados total (SS_total) para una matriz de rangos.
        
        Para una matriz de rangos completa, la suma de cuadrados total máxima es:
        SS_total = n * k * (k² - 1) / 12
        
        Returns:
            float: Suma de cuadrados total
        """
        n = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        # Fórmula para SS_total en matriz de rangos
        ss_total = n * k * (k * k - 1) / 12.0
        
        return ss_total

    def varianzaExplicadaDetallada(self) -> "Diccionario":
        """
        Calcula la varianza explicada con detalles de los componentes de varianza.
        
        Returns:
            Diccionario(str, float): Contiene:
            - "varianza_explicada": Proporción de varianza explicada (0-1)
            - "ss_tratamientos": Suma de cuadrados entre tratamientos
            - "ss_total": Suma de cuadrados total
            - "ss_error": Suma de cuadrados del error (SS_total - SS_tratamientos)
            - "coef_kendall": Coeficiente de Kendall (equivalente a varianza explicada)
            - "varianza_no_explicada": Proporción de varianza no explicada (1 - VE)
            - "bloques": Número de bloques
            - "tratamientos": Número de tratamientos
        """
        # Calcular componentes de varianza
        ve = self.varianzaExplicada()
        ss_tratamientos = self._calcularSumaCuadradosTratamientos()
        ss_total = self._calcularSumaCuadradosTotal()
        ss_error = ss_total - ss_tratamientos
        kendall = self.coefConcordKendall()
        ve_no_explicada = 1.0 - ve
        
        # Crear diccionario con resultados
        resultados = Diccionario(str, float)
        resultados["varianza_explicada"] = ve
        resultados["ss_tratamientos"] = ss_tratamientos
        resultados["ss_total"] = ss_total
        resultados["ss_error"] = ss_error
        resultados["coef_kendall"] = kendall
        resultados["varianza_no_explicada"] = ve_no_explicada
        resultados["bloques"] = float(self.filas)
        resultados["tratamientos"] = float(self.columnas)
        
        return resultados

    def interpretacionVarianzaExplicada(self, ve: float) -> str:
        """
        Proporciona una interpretación del valor de varianza explicada.
        
        Args:
            ve: Valor de varianza explicada (0-1)
            
        Returns:
            str: Interpretación del nivel de explicación
        """
        if ve < 0.1:
            return "Muy poca varianza explicada - efectos muy débiles"
        elif ve < 0.25:
            return "Poca varianza explicada - efectos débiles"
        elif ve < 0.5:
            return "Varianza explicada moderada - efectos moderados"
        elif ve < 0.75:
            return "Buena varianza explicada - efectos fuertes"
        elif ve < 0.9:
            return "Muy buena varianza explicada - efectos muy fuertes"
        else:
            return "Excelente varianza explicada - efectos casi determinísticos"

    def analisisVarianza(self) -> "Diccionario":
        """
        Realiza un análisis completo de varianza para la matriz de rangos.
        
        Returns:
            Diccionario(str, float): Análisis completo incluyendo:
            - Todos los componentes de varianzaExplicadaDetallada()
            - "interpretacion_num": Código numérico de interpretación (0-5)
            - "porcentaje_explicado": Varianza explicada como porcentaje
            - "estadistico_friedman": Estadístico de Friedman
            - "suma_rangos_str": Representación string de sumas de rangos
        """
        # Obtener análisis detallado de varianza
        detalle = self.varianzaExplicadaDetallada()
        
        # Obtener varianza explicada
        ve = detalle["varianza_explicada"]
        
        # Calcular interpretación numérica
        if ve < 0.1:
            interpretacion_num = 0  # Muy poca
        elif ve < 0.25:
            interpretacion_num = 1  # Poca
        elif ve < 0.5:
            interpretacion_num = 2  # Moderada
        elif ve < 0.75:
            interpretacion_num = 3  # Buena
        elif ve < 0.9:
            interpretacion_num = 4  # Muy buena
        else:
            interpretacion_num = 5  # Excelente
        
        # Calcular porcentaje
        porcentaje = ve * 100.0
        
        # Obtener estadístico de Friedman
        friedman = self.estadFriedman()
        
        # Obtener sumas de rangos
        sumas_rangos = self.sumaRangos()
        
        # Crear diccionario con resultados completos
        resultados = Diccionario(str, float)
        
        # Copiar resultados del análisis detallado
        for clave in detalle.keys():
            resultados[clave] = detalle[clave]
        
        # Agregar elementos adicionales
        resultados["interpretacion_num"] = float(interpretacion_num)
        resultados["porcentaje_explicado"] = porcentaje
        resultados["estadistico_friedman"] = friedman
        resultados["suma_rangos_str"] = str(sumas_rangos)
        
        return resultados

    def _obtenerValorCriticoNemenyi(self, k: int, alpha: float) -> float:
        """
        Obtiene el valor crítico q_α de la distribución del rango estudentizado
        para la prueba de Nemenyi.
        
        Args:
            k: Número de tratamientos
            alpha: Nivel de significancia
            
        Returns:
            float: Valor crítico q_α
        """
        # Tabla de valores críticos de la distribución del rango estudentizado
        # Estructura: {alpha: {k: q_valor}}
        tabla_critica = {
            0.05: {  # α = 0.05
                2: 1.960, 3: 2.344, 4: 2.569, 5: 2.728, 6: 2.850,
                7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164, 11: 3.219,
                12: 3.268, 13: 3.313, 14: 3.354, 15: 3.391, 16: 3.426,
                17: 3.458, 18: 3.489, 19: 3.517, 20: 3.544
            },
            0.01: {  # α = 0.01
                2: 2.576, 3: 3.031, 4: 3.314, 5: 3.521, 6: 3.685,
                7: 3.822, 8: 3.939, 9: 4.041, 10: 4.129, 11: 4.208,
                12: 4.279, 13: 4.343, 14: 4.402, 15: 4.456, 16: 4.506,
                17: 4.552, 18: 4.595, 19: 4.635, 20: 4.672
            },
            0.10: {  # α = 0.10
                2: 1.645, 3: 1.960, 4: 2.128, 5: 2.241, 6: 2.326,
                7: 2.394, 8: 2.450, 9: 2.498, 10: 2.539, 11: 2.576,
                12: 2.609, 13: 2.639, 14: 2.666, 15: 2.692, 16: 2.716,
                17: 2.738, 18: 2.759, 19: 2.779, 20: 2.797
            }
        }
        
        if alpha not in tabla_critica:
            raise ValueError(f"Nivel de significancia {alpha} no soportado. Use 0.01, 0.05, o 0.10")
        
        if k < 2 or k > 20:
            raise ValueError(f"Número de tratamientos {k} fuera de rango. Use entre 2 y 20")
        
        return tabla_critica[alpha][k]

    def _calcularDiferenciaCriticaNemenyi(self, alpha: float) -> float:
        """
        Calcula la diferencia crítica para la prueba de Nemenyi.
        
        Fórmula: CD = q_α √(k(k+1)/(6n))
        
        Args:
            alpha: Nivel de significancia
            
        Returns:
            float: Diferencia crítica
        """
        n = self.filas      # número de bloques
        k = self.columnas   # número de tratamientos
        
        # Obtener valor crítico
        q_alpha = self._obtenerValorCriticoNemenyi(k, alpha)
        
        # Calcular diferencia crítica
        cd = q_alpha * ((k * (k + 1)) / (6 * n)) ** 0.5
        
        return cd

    def nemenyi(self, alpha: float = 0.05) -> "Diccionario":
        """
        Realiza la prueba post-hoc de Nemenyi para comparaciones múltiples.
        
        La prueba de Nemenyi se utiliza después de una prueba de Friedman significativa
        para determinar qué pares de tratamientos difieren significativamente.
        
        Args:
            alpha: Nivel de significancia (0.01, 0.05, o 0.10)
            
        Returns:
            Diccionario(str, float): Contiene:
            - "diferencia_critica": Valor de la diferencia crítica
            - "alpha": Nivel de significancia usado
            - "q_critico": Valor crítico de la distribución
            - "comparaciones_significativas": Número de comparaciones significativas
            - "total_comparaciones": Número total de comparaciones
            - "matriz_diferencias_str": Matriz de diferencias absolutas (como string)
            - "matriz_significancia_str": Matriz de significancia (como string)
            - "suma_rangos_str": Sumas de rangos por tratamiento
        """
        # Verificar datos suficientes
        if self.filas < 2:
            raise ValueError("Se necesitan al menos 2 bloques para la prueba de Nemenyi")
        if self.columnas < 2:
            raise ValueError("Se necesitan al menos 2 tratamientos para la prueba de Nemenyi")
        
        # Calcular diferencia crítica
        cd = self._calcularDiferenciaCriticaNemenyi(alpha)
        q_critico = self._obtenerValorCriticoNemenyi(self.columnas, alpha)
        
        # Obtener sumas de rangos
        sumas_rangos = self.sumaRangos()
        
        # Crear matrices para almacenar resultados
        k = self.columnas
        matriz_diferencias = Matriz(k, k, float)
        matriz_significancia = Matriz(k, k, int)  # 1 = significativo, 0 = no significativo
        
        # Calcular todas las comparaciones por pares
        comparaciones_significativas = 0
        total_comparaciones = 0
        
        for i in range(k):
            for j in range(k):
                if i != j:
                    # Calcular diferencia absoluta entre sumas de rangos
                    diferencia_abs = abs(sumas_rangos[i] - sumas_rangos[j])
                    matriz_diferencias.modificar(i, j, diferencia_abs)
                    
                    # Determinar si es significativa
                    es_significativa = 1 if diferencia_abs > cd else 0
                    matriz_significancia.modificar(i, j, es_significativa)
                    
                    # Contar comparaciones (solo una vez por par)
                    if i < j:
                        total_comparaciones += 1
                        if es_significativa:
                            comparaciones_significativas += 1
                else:
                    # Diagonal: diferencia consigo mismo = 0, no significativa
                    matriz_diferencias.modificar(i, j, 0.0)
                    matriz_significancia.modificar(i, j, 0)
        
        # Crear diccionario con resultados
        resultados = Diccionario(str, float)
        resultados["diferencia_critica"] = cd
        resultados["alpha"] = alpha
        resultados["q_critico"] = q_critico
        resultados["comparaciones_significativas"] = float(comparaciones_significativas)
        resultados["total_comparaciones"] = float(total_comparaciones)
        resultados["bloques"] = float(self.filas)
        resultados["tratamientos"] = float(self.columnas)
        
        # Convertir matrices a string para almacenar
        resultados["matriz_diferencias_str"] = str(matriz_diferencias)
        resultados["matriz_significancia_str"] = str(matriz_significancia)
        resultados["suma_rangos_str"] = str(sumas_rangos)
        
        return resultados

    def nemenyiDetallado(self, alpha: float = 0.05) -> "Diccionario":
        """
        Realiza la prueba de Nemenyi con detalles extendidos de cada comparación.
        
        Args:
            alpha: Nivel de significancia
            
        Returns:
            Diccionario(str, float): Incluye todos los resultados de nemenyi() más:
            - "pares_significativos_str": Lista de pares significativos
            - "pares_no_significativos_str": Lista de pares no significativos
            - "interpretacion_num": Código de interpretación (0-4)
            - "proporcion_significativas": Proporción de comparaciones significativas
        """
        # Obtener resultados básicos
        resultados_basicos = self.nemenyi(alpha)
        
        # Obtener datos necesarios
        cd = resultados_basicos["diferencia_critica"]
        sumas_rangos = self.sumaRangos()
        k = self.columnas
        
        # Analizar cada par en detalle
        pares_significativos = []
        pares_no_significativos = []
        
        for i in range(k):
            for j in range(i + 1, k):  # Solo comparar cada par una vez
                diferencia_abs = abs(sumas_rangos[i] - sumas_rangos[j])
                es_significativa = diferencia_abs > cd
                
                par_info = f"T{i+1}-T{j+1}: |{sumas_rangos[i]:.1f} - {sumas_rangos[j]:.1f}| = {diferencia_abs:.2f}"
                
                if es_significativa:
                    pares_significativos.append(par_info + f" > {cd:.2f} (SIG)")
                else:
                    pares_no_significativos.append(par_info + f" ≤ {cd:.2f} (NS)")
        
        # Calcular interpretación
        total_comp = resultados_basicos["total_comparaciones"]
        sig_comp = resultados_basicos["comparaciones_significativas"]
        proporcion = sig_comp / total_comp if total_comp > 0 else 0.0
        
        if proporcion == 0:
            interpretacion_num = 0  # Ninguna diferencia
        elif proporcion < 0.25:
            interpretacion_num = 1  # Pocas diferencias
        elif proporcion < 0.5:
            interpretacion_num = 2  # Algunas diferencias
        elif proporcion < 0.75:
            interpretacion_num = 3  # Muchas diferencias
        else:
            interpretacion_num = 4  # Mayoría diferentes
        
        # Crear diccionario extendido
        resultados = Diccionario(str, float)
        
        # Copiar resultados básicos
        for clave in resultados_basicos.keys():
            resultados[clave] = resultados_basicos[clave]
        
        # Agregar detalles extendidos
        resultados["pares_significativos_str"] = str(pares_significativos)
        resultados["pares_no_significativos_str"] = str(pares_no_significativos)
        resultados["interpretacion_num"] = float(interpretacion_num)
        resultados["proporcion_significativas"] = proporcion
        
        return resultados

    def interpretacionNemenyi(self, proporcion_sig: float) -> str:
        """
        Interpreta los resultados de la prueba de Nemenyi.
        
        Args:
            proporcion_sig: Proporción de comparaciones significativas
            
        Returns:
            str: Interpretación del resultado
        """
        if proporcion_sig == 0:
            return "Ningún tratamiento difiere significativamente"
        elif proporcion_sig < 0.25:
            return "Pocas diferencias significativas entre tratamientos"
        elif proporcion_sig < 0.5:
            return "Algunas diferencias significativas detectadas"
        elif proporcion_sig < 0.75:
            return "Muchas diferencias significativas entre tratamientos"
        else:
            return "La mayoría de tratamientos difieren significativamente"

    def resumenNemenyi(self, alpha: float = 0.05) -> str:
        """
        Proporciona un resumen textual completo de la prueba de Nemenyi.
        
        Args:
            alpha: Nivel de significancia
            
        Returns:
            str: Resumen completo de los resultados
        """
        resultados = self.nemenyiDetallado(alpha)
        
        # Extraer datos
        cd = resultados["diferencia_critica"]
        sig_comp = int(resultados["comparaciones_significativas"])
        total_comp = int(resultados["total_comparaciones"])
        proporcion = resultados["proporcion_significativas"]
        
        # Crear resumen
        lineas = []
        lineas.append("=== PRUEBA POST-HOC DE NEMENYI ===")
        lineas.append(f"Nivel de significancia: α = {alpha}")
        lineas.append(f"Diferencia crítica: {cd:.4f}")
        lineas.append(f"Comparaciones significativas: {sig_comp}/{total_comp}")
        lineas.append(f"Proporción significativa: {proporcion:.2%}")
        lineas.append("")
        lineas.append(f"Interpretación: {self.interpretacionNemenyi(proporcion)}")
        lineas.append("")
        
        # Agregar detalles de pares si hay espacio
        if sig_comp > 0:
            lineas.append("Pares significativamente diferentes:")
            pares_sig_str = resultados["pares_significativos_str"]
            # Simplificar la representación de la lista
            pares_sig_str = pares_sig_str.replace("[", "").replace("]", "").replace("'", "")
            for par in pares_sig_str.split(", "):
                if par.strip():
                    lineas.append(f"  • {par.strip()}")
        
        return "\n".join(lineas)

class MatrizRachas:
    """
    MatrizRachas es una matriz de cadenas de rachas.
    Cada celda de la matriz es una cadena de rachas.
    Cada racha es una cadena de caracteres.
    """
    def __init__(self, bloques, tratamientos):
        self.datatype = Cadena
        self.bloques = bloques
        self.tratamientos = tratamientos
        self.data: Matriz = Matriz(len(bloques), len(tratamientos), Cadena)

    def _parse_indices(self, idx_str):
        """
        Parsea un string de índices tipo "i,j,k" o con "." como comodín.
        Devuelve una tupla de índices o None para comodines.
        """
        parts = idx_str.split(",")
        if len(parts) != 3:
            raise ValueError("Índices deben ser de la forma 'i,j,k' (usa '.' para comodines)")
        return tuple(None if p.strip() == "." else int(p) for p in parts)

    def _iter_indices(self, idx_tuple):
        """
        Genera todos los índices (i, j, k) válidos según el patrón de idx_tuple.
        """
        for i, bloque in enumerate(self.data):
            if idx_tuple[0] is not None and i != idx_tuple[0]:
                continue
            for j, trat in enumerate(bloque):
                if idx_tuple[1] is not None and j != idx_tuple[1]:
                    continue
                for k, racha in enumerate(trat):
                    if idx_tuple[2] is not None and k != idx_tuple[2]:
                        continue
                    yield(i, j, k)

    def getRacha(self, idx_str) -> int:
        """
        Devuelve el numero de racha en la posición (i, j, k).
        """
        i, j, k = self._parse_indices(idx_str)
        if not all(isinstance(x, int) for x in (i, j, k)):
            raise ValueError("traeRacha requiere índices específicos, no comodines y todos enteros")
        # Solo si i, j, k son enteros, hago las comparaciones y acceso
        if i is None or j is None or k is None:
            raise ValueError("traeRacha requiere índices específicos, no comodines y todos enteros")
        if i < 0 or i >= len(self.data):
            raise IndexError("Índice i fuera de rango")
        if j < 0 or j >= len(self.data[i]):
            raise IndexError("Índice j fuera de rango")
        if k < 0 or k >= len(self.data[i][j]):
            raise IndexError("Índice k fuera de rango")
        racha_cadena: Cadena = self.data[i][j]
        return racha_cadena.numRachas(k)

    def sumRachas(self, idx_str) -> int:
        """
        Suma todas las rachas en las posiciones indicadas por el patrón idx_str (puede usar "." como comodín).
        """
        idx_tuple = self._parse_indices(idx_str)
        total = 0
        for i, j, k in self._iter_indices(idx_tuple):
            if self.data[i][j] is None:
                raise ValueError("La celda no existe")
            cadena_racha: Cadena = self.data[i][j]
            conteo_rachas = cadena_racha.numRachas(k)
            total += conteo_rachas
        return total

    def promRachas(self, idx_str) -> float:
        """
        Promedia todas las rachas en las posiciones indicadas por el patrón idx_str (puede usar "." como comodín).
        """
        idx_tuple = self._parse_indices(idx_str)
        valores = []
        for i, j, k in self._iter_indices(idx_tuple):
            if self.data[i][j] is None:
                raise ValueError("La celda no existe")
            cadena_racha: Cadena = self.data[i][j]
            conteo_rachas = cadena_racha.numRachas(k)
            valores.append(conteo_rachas)
        if not valores:
            return 0.0
        return sum(valores) / len(valores)

    def modificaRacha(self, fila: int, columna: int, rachas: Cadena) -> None:
        """
        Modifica la racha en la posición [fila][columna], asignando la lista rachas.
        Cada elemento de rachas debe ser del tipo self.datatype.
        """
        if not (0 <= fila < len(self.data)):
            raise IndexError("Índice de fila fuera de rango")
        if not (0 <= columna < len(self.data[fila])):
            raise IndexError("Índice de columna fuera de rango")
        if not isinstance(rachas, Cadena):
            raise ValueError("rachas debe ser una cadena")
        for r in rachas:
            if not isinstance(r, self.datatype):
                raise ValueError(f"Cada elemento de rachas debe ser de tipo {self.datatype}")
        self.data[fila][columna] = rachas

    def __getitem__(self, fila: int):
        """
        Permite acceso como matriz_rachas[fila]. Devuelve una fila de la matriz.
        """
        if not (0 <= fila < len(self.data)):
            raise IndexError("Índice de fila fuera de rango")
        columna = Arreglo(Cadena)
        for val in self.data[fila]:
            columna.pushback(val)
        return columna

    def __setitem__(self, fila: int, valores: Arreglo) -> None:
        """
        Permite asignar una fila completa como matriz_rachas[fila] = valores.
        valores debe ser una lista de Python del tamaño de tratamientos, 
        donde cada elemento sea una Cadena.
        """
        if not (0 <= fila < len(self.data)):
            raise IndexError("Índice de fila fuera de rango")
        
        if not isinstance(valores, Arreglo):
            raise ValueError("valores debe ser un arreglo")
        
        if len(valores) != len(self.tratamientos):
            raise ValueError(f"La lista debe tener {len(self.tratamientos)} elementos (uno por tratamiento)")
        
        # Validar que cada elemento sea una Cadena
        for i, valor in enumerate(valores):
            if not isinstance(valor, Cadena):
                raise ValueError(f"El elemento en la posición {i} debe ser una Cadena, pero es {type(valor).__name__}")
        
        # Asignar los valores a la fila
        self.data[fila] = list(valores)

    @property
    def shape(self) -> tuple:
        return (len(self.bloques), len(self.tratamientos))

    def __add__(self, other: "MatrizRachas") -> "MatrizRachas":
        if not isinstance(other, MatrizRachas):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("Las matrices deben tener la misma forma para sumarse")
        if self.datatype != other.datatype:
            raise TypeError("Ambas matrices deben tener el mismo tipo de dato")
        nueva = MatrizRachas(self.bloques, self.tratamientos)
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # Concatenar las listas de réplicas
                nueva.data[i][j] = self.data[i][j] + other.data[i][j]
        return nueva

    def __iter__(self):
        for i, bloque in enumerate(self.data):
            for j, trat in enumerate(bloque):
                yield (i, j, self.data[i][j])

    def __repr__(self):
        return f"MatrizRachas(bloques={self.bloques}, tratamientos={self.tratamientos}, data={self.data})"

    def matrizNumRachas(self) -> "Matriz":
        """
        Convierte la MatrizRachas a una Matriz numérica donde cada celda contiene 
        el número de rachas. Esta matriz se puede usar para pruebas de Friedman.
        
        Returns:
            Matriz: Matriz numérica con el conteo de rachas por celda
        """
        matriz_numerica = Matriz(len(self.bloques), len(self.tratamientos), int)
        
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                cadena_rachas = self.data[i][j]
                if isinstance(cadena_rachas, Cadena):
                    # Contar el número de rachas en la cadena
                    num_rachas = cadena_rachas.numRachas()
                    matriz_numerica.modificar(i, j, num_rachas)
                else:
                    # Si no hay datos, asignar 0
                    matriz_numerica.modificar(i, j, 0)
        
        return matriz_numerica

    def promedioRachasPorCelda(self) -> "Matriz":
        """
        Para diseños con múltiples réplicas por celda, calcula el promedio 
        de rachas por celda según la fórmula: r̄ᵢ,ⱼ,• = (1/nᵢ,ⱼ) ∑rᵢ,ⱼ,ₖ
        
        En el diseño actual, cada celda tiene una cadena, así que retorna 
        el número de rachas directamente.
        
        Returns:
            Matriz: Matriz con promedios de rachas por celda
        """
        # Por ahora, como cada celda tiene una sola cadena, es igual al conteo
        matriz_numerica = Matriz(len(self.bloques), len(self.tratamientos), float)
        
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                cadena_rachas = self.data[i][j]
                if isinstance(cadena_rachas, Cadena):
                    # Contar el número de rachas en la cadena
                    prom_rachas:float = cadena_rachas.promRachas()
                    matriz_numerica.modificar(i, j, prom_rachas)

        return matriz_numerica

class Multicotomizacion:
    def __init__(self, categorias: Conjunto, datatype: type):
        check_datatypeA(datatype)
        self.categorias = categorias
        self.datatype = datatype
        self.reglas: List[Tuple[Callable[[object], bool], str]] = []

    def agnadeRegla(self, funcion, etiqueta: str) -> None:
        """
        Añade una regla de multicotomización: una función y la etiqueta asociada.
        La función debe aceptar un valor y devolver True/False.
        """
        self.reglas.append((funcion, etiqueta))

    def eliminarRegla(self, etiqueta: str) -> None:
        """
        Elimina la primera regla que tenga la etiqueta dada.
        """
        for i, (funcion, etq) in enumerate(self.reglas):
            if etq == etiqueta:
                del self.reglas[i]
                return
        raise ValueError(f"No existe una regla con la etiqueta '{etiqueta}'")

    def cadenaMulticotomizada(self, valores: Arreglo) -> "Cadena":
        """
        Dada una lista de valores, aplica las reglas en orden y devuelve una cadena con las etiquetas correspondientes.
        """
        resultado = ""
        for v in valores.data:
            if not isinstance(v, self.datatype):
                raise ValueError(f"El valor {v} no es del tipo {self.datatype}")
            etiqueta_encontrada = None
            for funcion, etiqueta in self.reglas:
                if funcion(v):
                    etiqueta_encontrada = etiqueta
                    break
            if etiqueta_encontrada is None:
                raise ValueError(f"Ninguna regla coincide para el valor {v}")
            resultado += etiqueta_encontrada
        return Cadena(resultado)

class M2VClasificacion:
    def __init__(self, paramGlobal, bloques: Arreglo, tratamientos: Arreglo, datatype: type):
        check_datatypeA(datatype)
        self.paramGlobal = paramGlobal
        self.bloques = bloques
        self.tratamientos = tratamientos
        self.datatype = datatype
        self.matriz = Matriz(len(bloques), len(tratamientos), Arreglo)
        self.matriz_rachas = None

    def modificar(self, fila: int, columna: int, valor) -> None:
        """
        Modifica el elemento en la posición [fila][columna] delegando a self.matriz.
        El valor debe ser un Arreglo cuyo datatype sea igual a self.datatype.
        """
        if not isinstance(valor, Arreglo):
            raise ValueError("El valor debe ser un Arreglo")
        if valor.datatype != self.datatype:
            raise ValueError(f"El Arreglo debe tener datatype {self.datatype}, pero tiene {valor.datatype}")
        self.matriz.modificar(fila, columna, valor)

    def __getitem__(self, fila: int):
        """
        Permite acceso como modelo[fila][columna] delegando a self.matriz.
        """
        return self.matriz[fila]

    def __setitem__(self, fila: int, valores):
        """
        Permite asignar una fila completa como modelo[fila] = valores delegando a self.matriz.
        valores debe ser un Arreglo que contiene elementos de tipo Arreglo con datatype igual a self.datatype.
        """
        # Validar que valores sea un Arreglo
        if not isinstance(valores, Arreglo):
            raise ValueError("valores debe ser un Arreglo")
        
        # Validar que el datatype del Arreglo valores sea Arreglo
        if valores.datatype != Arreglo:
            raise ValueError(f"El Arreglo valores debe tener datatype Arreglo, pero tiene {valores.datatype}")
        
        # Validar que cada elemento dentro del Arreglo sea un Arreglo con el datatype correcto
        for i, valor in enumerate(valores.data):
            if not isinstance(valor, Arreglo):
                raise ValueError(f"El elemento en la posición {i} debe ser un Arreglo")
            if valor.datatype != self.datatype:
                raise ValueError(f"El Arreglo en la posición {i} debe tener datatype {self.datatype}, pero tiene {valor.datatype}")
        
        self.matriz[fila] = valores.data

    def __repr__(self):
        """
        Representación string para debugging de M2VClasificacion
        """
        return (f"M2VClasificacion(paramGlobal={self.paramGlobal}, "
                f"bloques={repr(self.bloques)}, "
                f"tratamientos={repr(self.tratamientos)}, "
                f"datatype={self.datatype.__name__})")

    def __str__(self):
        """
        Representación string legible de M2VClasificacion mostrando la estructura y contenido
        """
        lineas = []
        lineas.append(f"M2VClasificacion:")
        lineas.append(f"  Parámetro Global: {self.paramGlobal}")
        lineas.append(f"  Tipo de Dato: {self.datatype.__name__}")
        lineas.append(f"  Bloques ({len(self.bloques)} elementos): {self.bloques}")
        lineas.append(f"  Tratamientos ({len(self.tratamientos)} elementos): {self.tratamientos}")
        lineas.append(f"  Matriz ({self.matriz.filas}x{self.matriz.columnas}):")
    
        # Mostrar la matriz con formato especial para arreglos
        for i in range(self.matriz.filas):
            elementos_fila = []
            for j in range(self.matriz.columnas):
                elemento = self.matriz.data[i][j]
                if elemento is None:
                    str_elemento = "None"
                elif isinstance(elemento, Arreglo):
                    # Mostrar contenido del arreglo de forma compacta
                    contenido = str(elemento.data) if elemento.data else "[]"
                    str_elemento = f"Arr{elemento.datatype.__name__}{contenido}"
                else:
                    str_elemento = str(elemento)
                elementos_fila.append(str_elemento)
            linea_matriz = "    [" + ", ".join(elementos_fila) + "]"
            lineas.append(linea_matriz)
        
        return "\n".join(lineas)

    def lleno(self) -> bool:
        """
        Devuelve True si ningún valor de la matriz es None y cada elemento 
        de la matriz es un Arreglo con datatype igual a self.datatype.
        En caso contrario devuelve False.
        """
        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas):
                elemento = self.matriz.data[i][j]
                
                # Verificar que el elemento no sea None
                if elemento is None:
                    return False
                
                # Verificar que el elemento sea un Arreglo
                if not isinstance(elemento, Arreglo):
                    return False
                
                # Verificar que el Arreglo tenga el datatype correcto
                if elemento.datatype != self.datatype:
                    return False
        
        return True

    def _extract_indices(self, index: str) -> tuple[int | None, int | None]:
        # Parsear el índice
        parts = index.split(",")
        if len(parts) != 2:
            raise ValueError("El índice debe ser de la forma 'x,y' (usa '.' para comodines)")
        
        x_str, y_str = [p.strip() for p in parts]
        
        # Convertir a índices o None para comodines
        if x_str == ".":
            x = None
        else:
            try:
                x = int(x_str)
                if x < 0 or x >= self.matriz.filas:
                    raise IndexError(f"Índice de fila {x} fuera de rango (0-{self.matriz.filas-1})")
            except ValueError:
                raise ValueError(f"'{x_str}' no es un índice válido. Use un entero o '.'")
        
        if y_str == ".":
            y = None
        else:
            try:
                y = int(y_str)
                if y < 0 or y >= self.matriz.columnas:
                    raise IndexError(f"Índice de columna {y} fuera de rango (0-{self.matriz.columnas-1})")
            except ValueError:
                raise ValueError(f"'{y_str}' no es un índice válido. Use un entero o '.'")
        
        return x, y

    def nDatos(self, index: str) -> int:
        """
        Calcula la suma de la cantidad de elementos internos de cada arreglo 
        en las posiciones especificadas por el índice.
        
        Args:
            index: String de la forma "x,y" donde:
                - x: fila (entero) o "." para todas las filas
                - y: columna (entero) o "." para todas las columnas
        
        Returns:
            int: Suma total de elementos en los arreglos especificados
        """
        x, y = self._extract_indices(index)
        
        # Calcular la suma de elementos
        total_elementos = 0
        
        # Determinar rango de filas
        if x is None:
            filas_rango = range(self.matriz.filas)
        else:
            filas_rango = range(x, x + 1)
        
        # Determinar rango de columnas
        if y is None:
            columnas_rango = range(self.matriz.columnas)
        else:
            columnas_rango = range(y, y + 1)
        
        # Iterar sobre las posiciones especificadas
        for i in filas_rango:
            for j in columnas_rango:
                elemento = self.matriz.data[i][j]
                
                # Verificar que el elemento sea un Arreglo
                if not isinstance(elemento, Arreglo):
                    raise TypeError(f"El elemento en la posición [{i}][{j}] no es un Arreglo, es {type(elemento).__name__}")
                
                total_elementos += len(elemento.data)
        
        return total_elementos

    def datos(self, index: str) -> "Conjunto":
        """
        Retorna un Conjunto que une todos los elementos encontrados en las 
        posiciones especificadas por el índice.
        
        Args:
            index: String de la forma "x,y" donde:
                - x: fila (entero) o "." para todas las filas
                - y: columna (entero) o "." para todas las columnas
        
        Returns:
            Conjunto: Nuevo Conjunto con datatype self.datatype que contiene 
                     todos los elementos unidos de las posiciones especificadas
        """
        x, y = self._extract_indices(index)
        
        # Crear un nuevo Conjunto para almacenar todos los elementos
        resultado: Conjunto = Conjunto(self.datatype)
        
        # Determinar rango de filas
        if x is None:
            filas_rango = range(self.matriz.filas)
        else:
            filas_rango = range(x, x + 1)
        
        # Determinar rango de columnas
        if y is None:
            columnas_rango = range(self.matriz.columnas)
        else:
            columnas_rango = range(y, y + 1)
        
        # Iterar sobre las posiciones especificadas
        for i in filas_rango:
            for j in columnas_rango:
                elemento = self.matriz.data[i][j]
                
                # Verificar que el elemento sea un Conjunto
                if not isinstance(elemento, Arreglo):
                    raise TypeError(f"El elemento en la posición [{i}][{j}] no es un Arreglo, es {type(elemento).__name__}")
                
                # Agregar todos los elementos del Conjunto al resultado
                for item in elemento.data:
                    resultado.add(item)
        
        return resultado

    def getMatrizRachas(self, modeloMulticotomizado: Multicotomizacion) -> "MatrizRachas":
        """
        Genera una MatrizRachas aplicando multicotomización a cada arreglo de la matriz
        y convirtiendo las rachas de strings a listas de caracteres.
        
        Args:
            modeloMulticotomizado: Objeto Multicotomizacion con las reglas definidas
            
        Returns:
            MatrizRachas: Nueva matriz donde cada posición contiene rachas como listas de caracteres
        """  
        # Crear MatrizRachas con las mismas dimensiones, usando str como datatype para caracteres
        matriz_rachas = MatrizRachas(self.bloques.data, self.tratamientos.data)
        
        # Procesar cada posición de la matriz
        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas):
                elemento = self.matriz.data[i][j]
                
                # Verificar que el elemento sea un Arreglo válido
                if isinstance(elemento, Arreglo) and elemento.datatype == self.datatype:
                    # Aplicar multicotomización a los datos del arreglo
                    cadena_multicotomizada: Cadena = modeloMulticotomizado.cadenaMulticotomizada(elemento)
                    
                    # Obtener las rachas como subcadenas
                    matriz_rachas.modificaRacha(i, j, cadena_multicotomizada)
        
        self.matriz_rachas = matriz_rachas
        return matriz_rachas