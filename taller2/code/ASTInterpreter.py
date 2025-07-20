import warnings

import TDA
import lexer

class ProgramNode:
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

    def eval(self, env):
        env['data_local'] = []
        env['data'] = []
        env["stack"] = []
        for statement in self.statements:
            statement.eval(env)


class MainNode:
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"MainNode(statements={self.statements})"

    def eval(self, env):
        env['stack'] = ['Principal']
        for statement in self.statements:
            statement.eval(env)


class FuncNode:
    def __init__(self, datatypes: list[str], ID: str,
                 params: list[tuple[list, str]], body: list):
        self.datatypes = datatypes
        self.ID = ID
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FuncNode(datatypes={self.datatypes}, ID={self.ID}, params={self.params}, body={self.body})"

    def eval(self, env):
        """
        Adds the function to the environment.
        """
        if self.ID in env:
            raise ValueError(f"'{self.ID}' already defined. Can't define function with the same ID (name)")
        func_dict = {
            "datatypes": self.datatypes,
            "params": self.params,
            "body": self.body,
            "data": None
        }
        env[self.ID] = func_dict


class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

    def eval(self, env):
        """
        Evaluates the expression and prints the result.
        """
        value = self.expression.eval(env)
        print(value)  # Assuming the expression has an eval method


def handle_type_a(datatype: str, value):
    if not isinstance(datatype, str):
        raise TypeError("Tipo de dato vacío o mal formado")

    tipo_actual = datatype[0]

    # Caso base: tipo simple
    tipo_map = {
        'Entero': int,
        'Flotante': float,
        'Complejo': complex,
        'Cadena': TDA.Cadena,
        'Caracter': TDA.Cadena,
        'Bool': bool
    }
    py_type = tipo_map.get(tipo_actual)
    if py_type is None:
        raise TypeError(f"Tipo simple '{tipo_actual}' no soportado")
    if not isinstance(value, py_type):
        raise ValueError(f"El valor debe ser instancia de {tipo_actual} y el interno debe ser {py_type}")
    return value

def handle_conjunto_arreglo(datatypes: list[str], value) -> TDA.Arreglo | TDA.Conjunto:
    if len(datatypes) < 2:
        raise TypeError("Tipo de dato vacío o mal formado")

    tipo_contenedor = datatypes[0]
    
    # Resolver el tipo interno recursivamente
    def resolve_inner_type(types_list):
        """Resuelve el tipo interno desde la lista de tipos"""
        if len(types_list) == 1:
            # Tipo base (TiposA)
            tipo_map = {
                'Entero': int,
                'Flotante': float,
                'Complejo': complex,
                'Cadena': TDA.Cadena,
                'Caracter': TDA.Cadena,
                'Bool': bool
            }
            return tipo_map.get(types_list[0])
        else:
            # Para tipos anidados, retornamos la clase TDA correspondiente (TiposB)
            tipo_contenedores = {
                'Arreglo': TDA.Arreglo,
                'Conjunto': TDA.Conjunto,
                'Diccionario': TDA.Diccionario,
                'Matriz': TDA.Matriz,
                'MatrizRachas': TDA.MatrizRachas,
                'Multicotomizacion': TDA.Multicotomizacion,
                'M2VClasificacion': TDA.M2VClasificacion
            }
            tipo_class = tipo_contenedores.get(types_list[0])
            if tipo_class is None:
                raise TypeError(f"Tipo contenedor '{types_list[0]}' no soportado")
            return tipo_class

    # Obtener el tipo para el constructor
    inner_type = resolve_inner_type(datatypes[1:])

    if tipo_contenedor == 'Arreglo':
        new_value: TDA.Arreglo = None

        if value is None:
            # Crear arreglo vacío del tipo correspondiente
            new_value = TDA.Arreglo(inner_type)
        elif not isinstance(value, TDA.Arreglo):
            if not isinstance(value, list):
                raise ValueError(f"El valor debe ser instancia de {tipo_contenedor} o una lista")
            else:
                # Crear arreglo y poblar con elementos de la lista
                new_value = TDA.Arreglo(inner_type)
                for elem in value:
                    # Para elementos anidados, llamar recursivamente
                    if len(datatypes) > 2:  # Hay más niveles de anidamiento
                        processed_elem = handle_conjunto_arreglo(datatypes[1:], elem)
                    else:  # Tipo base
                        processed_elem = handle_type_a(datatypes[1], elem)
                    new_value.pushback(processed_elem)
        else:
            # Validar que el arreglo existente tenga el tipo correcto
            if value.datatype != inner_type:
                raise ValueError(f"El valor debe ser instancia de {tipo_contenedor} con tipo interno {inner_type}, no {value.datatype}")
            new_value = value

    elif tipo_contenedor == 'Conjunto':
        new_value: TDA.Conjunto = None

        if value is None:
            # Crear conjunto vacío del tipo correspondiente
            new_value = TDA.Conjunto(inner_type)
        elif not isinstance(value, TDA.Conjunto):
            if not isinstance(value, list):
                raise ValueError(f"El valor debe ser instancia de {tipo_contenedor} o una lista")
            else:
                # Crear conjunto y poblar con elementos de la lista
                new_value = TDA.Conjunto(inner_type)
                for elem in value:
                    # Para elementos anidados, llamar recursivamente
                    if len(datatypes) > 2:  # Hay más niveles de anidamiento
                        processed_elem = handle_conjunto_arreglo(datatypes[1:], elem)
                    else:  # Tipo base
                        processed_elem = handle_type_a(datatypes[1], elem)
                    new_value.add(processed_elem)
        else:
            # Validar que el conjunto existente tenga el tipo correcto
            if value.datatype != inner_type:
                raise ValueError(f"El valor debe ser instancia de {tipo_contenedor} con tipo interno {inner_type}, no {value.datatype}")
            new_value = value
    
    return new_value

def handle_diccionario(datatype_key: str, datatype_value: str, value) -> TDA.Diccionario:

    if value is None:
        new_value = TDA.Diccionario(datatype_key, datatype_value)
    elif not isinstance(value, TDA.Diccionario):
        if not isinstance(value, dict):
            raise ValueError(f"El valor debe ser instancia de diccionario o un diccionario")
        else:
            new_value = TDA.Diccionario(datatype_key, datatype_value)
            for key, val in value.items():
                key = handle_type_a(datatype_key, key)
                new_value[key] = handle_type_a(datatype_value, val)
    else:
        if value.key_datatype != datatype_key or value.value_datatype != datatype_value:
            raise ValueError(f"El valor debe ser instancia de diccionario y la clave debe ser de tipo {datatype_key} y el valor debe ser de tipo {datatype_value}")
        new_value = value.copy()

    return new_value

def handle_matriz(filas: int|None, columnas: int|None, datatype: str, value) -> TDA.Matriz:
    if value is None:
        new_value = TDA.Matriz(filas, columnas, datatype)
    elif not isinstance(value, TDA.Matriz):
        if not isinstance(value, list):
            raise ValueError(f"El valor debe ser instancia de matriz o una lista")
        else:
            new_value = TDA.Matriz(filas, columnas, datatype)
            for i in range(filas):
                for j in range(columnas):
                    new_value.modificar(i, j, value[i][j])
    else:
        new_value = value.copy()

    return new_value

def handle_matriz_rachas(bloques: int|None, tratamientos: int|None, datatype: str, value) -> TDA.MatrizRachas:
    if value is None:
        new_value = TDA.MatrizRachas(bloques, tratamientos)
    elif not isinstance(value, TDA.MatrizRachas):
        raise ValueError(f"El valor debe ser instancia de matriz de rachas o una lista")
    else:
        new_value = value.copy()
    return new_value

def handle_multicotomizacion(categorias: list[str] | None, datatype: str | None, value) -> TDA.Multicotomizacion:
    if value is None:
        new_value = TDA.Multicotomizacion(categorias, datatype)
    elif not isinstance(value, TDA.Multicotomizacion):
        raise ValueError(f"El valor debe ser instancia de multicotomización o una lista")
    else:
        new_value = value.copy()
    return new_value

def handle_m2v_clasificacion(paramGlobal: str | None, bloques: list[str] | None, tratamientos: list[str] | None, datatype: str, value) -> TDA.M2VClasificacion:
    if value is None:
        new_value = TDA.M2VClasificacion(paramGlobal, bloques, tratamientos, datatype)
    elif not isinstance(value, TDA.M2VClasificacion):
        raise ValueError(f"El valor debe ser instancia de m2v clasificación o una lista")
    else:
        new_value = value.copy()
    return new_value

def check_and_convert(value, datatype):
    # datatype es una lista, ej: ['Arreglo', 'Arreglo', 'Entero']

    if not datatype:
        raise TypeError("Tipo de dato vacío o mal formado")

   #elif tipo_actual in lexer.tiposb:
    elif len(datatype) > 1:
        tipo_interno = datatype[-1]
        tipo_contenedor = datatype[-2]

        if tipo_interno not in lexer.tiposa:
            raise TypeError(f"Tipo interno '{tipo_interno}' no soportado")
        if tipo_contenedor not in lexer.tiposb:
            raise TypeError(f"Tipo contenedor '{tipo_contenedor}' no soportado")

        # Caso recursivo: contenedor
        tiposb_clases = {
            'MatrizRachas': TDA.MatrizRachas,
            'Multicotomizacion': TDA.Multicotomizacion,
            'M2VClasificacion': TDA.M2VClasificacion,
            'Conjunto': TDA.Conjunto,
            'Arreglo': TDA.Arreglo,
            'Matriz': TDA.Matriz,
            'Diccionario': TDA.Diccionario
        }
        expected_class = tiposb_clases.get(tipo_actual)
        if expected_class is None:
            raise TypeError(f"Tipo contenedor '{tipo_actual}' no soportado")
        if not isinstance(value, expected_class):
            raise TypeError(f"El valor debe ser instancia de {tipo_actual}")

        '''# Si hay tipo interno, valida recursivamente los elementos internos
        if tipo_restante:
            # Ejemplo para Arreglo: asume que value tiene un atributo 'elementos' o es iterable
            if tipo_actual in ['Arreglo', 'Conjunto', 'Matriz']:
                # Recursivamente valida cada elemento
                for elem in value:  # O value.elementos, según tu implementación
                    check_and_convert(elem, tipo_restante)
            # Para Diccionario, podrías validar keys y values por separado si tu gramática lo permite
            # Para los otros tiposb abstractos, puedes decidir si requieren validación interna'''
        return value

    else:
        raise TypeError(f"Tipo '{tipo_actual}' no reconocido")


class VariableDeclaration:
    def __init__(self, datatype: list[str], ID: str, expression):
        self.datatype = datatype
        self.ID = ID
        self.expression = expression

    def __repr__(self):
        return f"VariableNode(datatype={self.datatype}, ID={self.ID}, expression={self.expression})"

    def eval(self, env):
        """
        Adds the variable to the environment.
        """
        if self.ID in env['data_local'].keys() or self.ID in env['data'].keys():
            raise ValueError(f"'{self.ID}' already defined. Can't define variable with the same ID (name)")

        try:
            value = self.expression.eval(env)
        except AttributeError:
            value = self.expression
            warnings.warn(f"Expression {self.expression} does not have an eval method, using expression directly")

        if len(self.datatype) == 1 and self.datatype[0] in lexer.tiposa:
            value = handle_type_a(self.datatype[0], value)
        elif len(self.datatype) > 1:
            value = handle_conjunto_arreglo(self.datatype, value)
        else:
            raise TypeError("Declaración mal formada")

        env['data_local'][self.ID] =(self.datatype, value)  # Guarda el valor convertido o validado


def create_type_instance(datatypes: list[str], arg_list: list = None) -> object:
    """
    Crea una instancia del tipo especificado por datatypes, manejando tipos anidados recursivamente.
    
    Args:
        datatypes: Lista de tipos, ej: ["Arreglo", "Diccionario", "Cadena", "Entero"]
        arg_list: Lista de argumentos adicionales para tipos que los requieren
    
    Returns:
        Instancia del tipo especificado
    """
    if not datatypes:
        raise TypeError("Lista de tipos vacía")
    
    tipo_principal = datatypes[0]
    
    # Tipos básicos (TiposA)
    if len(datatypes) == 1:
        tipo_map = {
            'Entero': lambda: 0,
            'Flotante': lambda: 0.0,
            'Complejo': lambda: 0+0j,
            'Cadena': lambda: TDA.Cadena(""),
            'Caracter': lambda: TDA.Cadena(""),
            'Bool': lambda: False
        }
        creator = tipo_map.get(tipo_principal)
        if creator:
            return creator()
        else:
            raise TypeError(f"Tipo básico '{tipo_principal}' no soportado")
    
    # Tipos contenedores (TiposB)
    if tipo_principal == 'Arreglo':
        # Para arreglos, el tipo interno es el resto de la lista
        inner_type = resolve_datatype_for_constructor(datatypes[1:])
        return TDA.Arreglo(inner_type)
    
    elif tipo_principal == 'Conjunto':
        # Para conjuntos, el tipo interno es el resto de la lista
        inner_type = resolve_datatype_for_constructor(datatypes[1:])
        return TDA.Conjunto(inner_type)
    
    elif tipo_principal == 'Diccionario':
        # Para diccionarios: Diccionario<TipoClave, TipoValor>
        if len(datatypes) < 3:
            raise TypeError("Diccionario requiere al menos 2 tipos internos")
        key_type = resolve_datatype_for_constructor([datatypes[1]])
        value_type = resolve_datatype_for_constructor([datatypes[2]])
        return TDA.Diccionario(key_type, value_type)
    
    elif tipo_principal == 'Matriz':
        # Para matrices: Matriz<TipoElemento> con filas y columnas de arg_list
        if len(datatypes) < 2:
            raise TypeError("Matriz requiere tipo interno")
        if not arg_list or len(arg_list) < 2:
            raise TypeError("Matriz requiere filas y columnas en arg_list")
        element_type = resolve_datatype_for_constructor([datatypes[1]])
        return TDA.Matriz(arg_list[0], arg_list[1], element_type)
    
    elif tipo_principal == 'MatrizRachas':
        # Para MatrizRachas con bloques y tratamientos de arg_list
        if not arg_list or len(arg_list) < 2:
            raise TypeError("MatrizRachas requiere bloques y tratamientos en arg_list")
        return TDA.MatrizRachas(arg_list[0], arg_list[1])
    
    elif tipo_principal == 'Multicotomizacion':
        # Para Multicotomizacion con categorías y datatype de arg_list
        if not arg_list or len(arg_list) < 2:
            raise TypeError("Multicotomizacion requiere categorías y datatype en arg_list")
        return TDA.Multicotomizacion(arg_list[0], arg_list[1])
    
    elif tipo_principal == 'M2VClasificacion':
        # Para M2VClasificacion con parámetros de arg_list
        if not arg_list or len(arg_list) < 4:
            raise TypeError("M2VClasificacion requiere paramGlobal, bloques, tratamientos y datatype en arg_list")
        return TDA.M2VClasificacion(arg_list[0], arg_list[1], arg_list[2], arg_list[3])
    
    else:
        raise TypeError(f"Tipo contenedor '{tipo_principal}' no soportado")

def resolve_datatype_for_constructor(datatypes: list[str]) -> type:
    """
    Resuelve una lista de tipos a un tipo de Python para usar en constructores.
    Similar a resolve_inner_type pero maneja todos los casos.
    """
    if not datatypes:
        raise TypeError("Lista de tipos vacía")
    
    if len(datatypes) == 1:
        # Tipo básico
        tipo_map = {
            'Entero': int,
            'Flotante': float,
            'Complejo': complex,
            'Cadena': TDA.Cadena,
            'Caracter': TDA.Cadena,
            'Bool': bool
        }
        py_type = tipo_map.get(datatypes[0])
        if py_type:
            return py_type
        else:
            raise TypeError(f"Tipo básico '{datatypes[0]}' no soportado")
    
    # Tipo contenedor
    tipo_contenedores = {
        'Arreglo': TDA.Arreglo,
        'Conjunto': TDA.Conjunto,
        'Diccionario': TDA.Diccionario,
        'Matriz': TDA.Matriz,
        'MatrizRachas': TDA.MatrizRachas,
        'Multicotomizacion': TDA.Multicotomizacion,
        'M2VClasificacion': TDA.M2VClasificacion
    }
    tipo_class = tipo_contenedores.get(datatypes[0])
    if tipo_class:
        return tipo_class
    else:
        raise TypeError(f"Tipo contenedor '{datatypes[0]}' no soportado")

class GenericVariableDeclNode:
    def __init__(self, datatype: list[str], ID: str, arg_list: list):
        self.datatype = datatype
        self.ID = ID
        self.arg_list = arg_list

    def __repr__(self):
        return f"GenericVariableDeclNode(datatype={self.datatype}, ID={self.ID}, arg_list={self.arg_list})"

    def eval(self, env):
        """
        Adds the variable to the environment.
        """
        if self.ID in env['data_local'].keys() or self.ID in env['data'].keys():
            raise ValueError(f"'{self.ID}' already defined. Can't define variable with the same ID (name)")

        # Usar la función general para crear cualquier tipo recursivamente
        value = create_type_instance(self.datatype, self.arg_list)
        
        env['data_local'][self.ID] = (self.datatype, value)  # Guarda el valor convertido o validado
