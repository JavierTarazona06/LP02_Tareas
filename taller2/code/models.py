# Clases agregadas para tiposb contenedores
from typing import Callable, List, Tuple

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

class Conjunto:
    def __init__(self, datatype: type) -> None:
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
        self.datatype = datatype
        self.data = []

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
        if not isinstance(value, self.datatype):
            raise ValueError(f"El valor debe ser de tipo {self.datatype}")
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

class Matriz:
    def __init__(self, *args, **kwargs):
        pass
    # TODO: Implementar métodos y atributos específicos

class Diccionario:
    def __init__(self, *args, **kwargs):
        pass
    # TODO: Implementar métodos y atributos específicos 

class MatrizRachas:
    def __init__(self, bloques, tratamientos, datatype: type):
        self.bloques = bloques
        self.tratamientos = tratamientos
        self.data = []
        self.datatype = datatype
        for b in bloques:
            bloque = []
            for t in tratamientos:
                bloque.append([])  # Ahora cada celda es una lista de réplicas
            self.data.append(bloque)

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

    def traeRacha(self, idx_str):
        """
        Devuelve la racha en la posición (i, j, k).
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
        return self.data[i][j][k]

    def sumRachas(self, idx_str):
        """
        Suma todas las rachas en las posiciones indicadas por el patrón idx_str (puede usar "." como comodín).
        """
        idx_tuple = self._parse_indices(idx_str)
        total = 0
        for i, j, k in self._iter_indices(idx_tuple):
            racha = self.data[i][j][k]
            if racha is not None:
                total += racha
        return total

    def promRachas(self, idx_str):
        """
        Promedia todas las rachas en las posiciones indicadas por el patrón idx_str (puede usar "." como comodín).
        """
        idx_tuple = self._parse_indices(idx_str)
        valores = []
        for i, j, k in self._iter_indices(idx_tuple):
            racha = self.data[i][j][k]
            if racha is not None:
                valores.append(racha)
        if not valores:
            return 0.0
        return sum(valores) / len(valores)

    def modificaRacha(self, fila: int, columna: int, rachas: list) -> None:
        """
        Modifica la racha en la posición [fila][columna], asignando la lista rachas.
        Cada elemento de rachas debe ser del tipo self.datatype.
        """
        if not (0 <= fila < len(self.data)):
            raise IndexError("Índice de fila fuera de rango")
        if not (0 <= columna < len(self.data[fila])):
            raise IndexError("Índice de columna fuera de rango")
        if not isinstance(rachas, list):
            raise ValueError("rachas debe ser una lista")
        for r in rachas:
            if not isinstance(r, self.datatype):
                raise ValueError(f"Cada elemento de rachas debe ser de tipo {self.datatype}")
        self.data[fila][columna] = rachas

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
        nueva = MatrizRachas(self.bloques, self.tratamientos, self.datatype)
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

class Multicotomizacion:
    def __init__(self, categorias: Conjunto, datatype: type):
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

    def cadenaMulticotomizada(self, valores: list) -> str:
        """
        Dada una lista de valores, aplica las reglas en orden y devuelve una cadena con las etiquetas correspondientes.
        """
        resultado = ""
        for v in valores:
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
        return resultado

class M2VClasificacion:
    def __init__(self, *args, **kwargs):
        pass
    # TODO: Implementar métodos y atributos específicos