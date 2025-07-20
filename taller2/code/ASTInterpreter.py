import lexer
import TDA


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


class StringNode:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode(value={self.value})"

    def eval(self, env):
        return self.value

def check_and_convert(value, datatype):
    # datatype es una lista, ej: ['Arreglo', 'Arreglo', 'Entero']

    if not datatype:
        raise TypeError("Tipo de dato vacío o mal formado")

    tipo_actual = datatype[-1]
    tipo_restante = datatype[:-1]

    if tipo_actual in lexer.tiposa:
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
            try:
                value = py_type(value)
            except Exception:
                raise TypeError(f"No se puede convertir '{value}' a {tipo_actual}")
        return value

    elif tipo_actual in lexer.tiposb:
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

        value = self.expression.eval(env)
        value = check_and_convert(value, self.datatype)
        env['data_local'][self.ID] =(self.datatype, value)  # Guarda el valor convertido o validado


# TODO Jugar con la semantica y la ejecución
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
        if self.ID in env:
            raise ValueError(f"'{self.ID}' already defined. Can't define variable with the same ID (name)")
        env[self.ID] = None  # Initialize variable with None or appropriate default value
