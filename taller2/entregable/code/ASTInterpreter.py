import warnings

import TDA
import lexer

# =============================================================================
# UTILITY FUNCTIONS FOR TYPE CONVERSION
# =============================================================================

def python_type_to_language_type_list(python_type):  
    """
    Convierte un tipo Python a lista de tipos del lenguaje, manejando tipos anidados recursivamente.
    
    Args:
        python_type: Tipo Python (int, float, TDA.Arreglo, etc.)
    
    Returns:
        list[str]: Lista de strings representando los tipos del lenguaje
        
    Examples:
        int → ["Entero"]
        TDA.Arreglo(int) → ["Arreglo", "Entero"]
        TDA.Diccionario(TDA.Cadena, int) → ["Diccionario", "Cadena", "Entero"]
    """
    # Mapeo de tipos básicos Python a tipos del lenguaje
    basic_type_mapping = {
        int: 'Entero',
        float: 'Flotante', 
        bool: 'Bool',
        complex: 'Complejo',
        str: 'Cadena'
    }
    
    # Si es un tipo básico Python
    if python_type in basic_type_mapping:
        return [basic_type_mapping[python_type]]
    
    # Si es una clase TDA
    if hasattr(python_type, '__name__'):
        class_name = python_type.__name__
        
        # Tipos TDA básicos
        if class_name == 'Cadena':
            return ['Cadena']
        
        # Tipos TDA contenedores
        elif class_name in ['Arreglo', 'Conjunto']:
            # Para objetos Arreglo/Conjunto, obtener su tipo interno
            if hasattr(python_type, 'datatype'):
                inner_type = python_type_to_language_type_list(python_type.datatype)
                return [class_name] + inner_type
            else:
                # Si no tiene datatype, asumir tipo básico
                return [class_name, 'Entero']  # Default fallback
        
        elif class_name == 'Diccionario':
            # Para Diccionario, necesitamos tanto key_datatype como value_datatype
            if hasattr(python_type, 'key_datatype') and hasattr(python_type, 'value_datatype'):
                key_type = python_type_to_language_type_list(python_type.key_datatype)
                value_type = python_type_to_language_type_list(python_type.value_datatype)
                return ['Diccionario'] + key_type + value_type
            else:
                return ['Diccionario', 'Cadena', 'Entero']  # Default fallback
        
        elif class_name == 'Matriz':
            # Para Matriz, obtener su tipo interno
            if hasattr(python_type, 'datatype'):
                inner_type = python_type_to_language_type_list(python_type.datatype)
                return ['Matriz'] + inner_type
            else:
                return ['Matriz', 'Entero']  # Default fallback
        
        # Otros tipos TDA específicos
        elif class_name in ['MatrizRachas', 'Multicotomizacion', 'M2VClasificacion']:
            return [class_name]
    
    # Si es una instancia de objeto TDA, obtener su tipo de clase
    if hasattr(python_type, '__class__'):
        return python_type_to_language_type_list(python_type.__class__)
    
    # Fallback para tipos no reconocidos
    return ['Entero']


def python_type_to_language_type_string(python_type):
    """
    Convierte un tipo Python simple a string del lenguaje (solo para tipos básicos).
    
    Args:
        python_type: Tipo Python básico (int, float, bool, etc.)
    
    Returns:
        str: String del tipo del lenguaje
        
    Examples:
        int → "Entero"
        float → "Flotante"
        TDA.Cadena → "Cadena"
    """
    type_mapping = {
        int: 'Entero',
        float: 'Flotante', 
        bool: 'Bool',
        complex: 'Complejo',
        str: 'Cadena'
    }
    
    # Si es una clase TDA, usar su nombre
    if hasattr(python_type, '__name__'):
        if python_type.__name__ == 'Cadena':
            return 'Cadena'
    
    return type_mapping.get(python_type, 'Entero')  # Default fallback


def language_type_to_python_type(tipo_str: str):
    """
    Convierte un string del tipo del lenguaje a tipo Python.
    
    Args:
        tipo_str: String del tipo del lenguaje
    
    Returns:
        type: Tipo Python correspondiente
        
    Examples:
        "Entero" → int
        "Flotante" → float
        "Cadena" → TDA.Cadena
    """
    type_mapping = {
        'Entero': int,
        'Flotante': float,
        'Bool': bool,
        'Complejo': complex,
        'Cadena': TDA.Cadena,
        'Caracter': TDA.Cadena,  # Caracter se trata como Cadena
        'Arreglo': TDA.Arreglo,
        'Conjunto': TDA.Conjunto,
        'Diccionario': TDA.Diccionario,
        'Matriz': TDA.Matriz,
        'MatrizRachas': TDA.MatrizRachas,
        'Multicotomizacion': TDA.Multicotomizacion,
        'M2VClasificacion': TDA.M2VClasificacion
    }
    
    if tipo_str not in type_mapping:
        raise ValueError(f"Tipo '{tipo_str}' no reconocido")
    
    return type_mapping[tipo_str]


def language_type_list_to_python_type(datatype_list: list[str]):
    """
    Convierte una lista de tipos del lenguaje a tipo Python, manejando tipos anidados.
    
    Args:
        datatype_list: Lista de strings de tipos del lenguaje
    
    Returns:
        type: Tipo Python correspondiente (puede ser complejo para contenedores)
        
    Examples:
        ["Entero"] → int
        ["Arreglo", "Entero"] → TDA.Arreglo con datatype=int
        ["Diccionario", "Cadena", "Entero"] → TDA.Diccionario con key_datatype=TDA.Cadena, value_datatype=int
    """
    if not datatype_list:
        return int  # Default fallback
    
    main_type = datatype_list[0]
    
    # Tipos básicos
    if len(datatype_list) == 1:
        return language_type_to_python_type(main_type)
    
    # Tipos contenedores
    elif main_type in ['Arreglo', 'Conjunto']:
        # Para Arreglo/Conjunto, el tipo interno está en datatype_list[1:]
        inner_type = language_type_list_to_python_type(datatype_list[1:])
        container_class = language_type_to_python_type(main_type)
        # Nota: Esto retorna la clase, no una instancia. La instancia se crea en tiempo de ejecución.
        return container_class
    
    elif main_type == 'Diccionario':
        # Para Diccionario, necesitamos separar key_type y value_type
        # Formato: ["Diccionario", "KeyType", "ValueType"]
        if len(datatype_list) >= 3:
            key_type = language_type_to_python_type(datatype_list[1])
            value_type = language_type_to_python_type(datatype_list[2])
            return TDA.Diccionario
        else:
            return TDA.Diccionario
    
    elif main_type == 'Matriz':
        # Para Matriz, el tipo interno está en datatype_list[1:]
        inner_type = language_type_list_to_python_type(datatype_list[1:])
        return TDA.Matriz
    
    else:
        # Otros tipos especiales
        return language_type_to_python_type(main_type)

def handle_type_a_conversion(datatype_str: str, value):
    """
    Convierte y valida un valor al tipo básico especificado (TiposA).
    
    Args:
        datatype_str: String del tipo ("Entero", "Flotante", etc.)
        value: Valor a convertir
        
    Returns:
        Valor convertido al tipo correcto
        
    Raises:
        TypeError: Si el tipo no es soportado
        ValueError: Si el valor no se puede convertir
    """
    if not isinstance(datatype_str, str):
        raise TypeError("Tipo de dato debe ser string")
    
    # Mapeo de tipos de lenguaje a tipos Python
    type_conversions = {
        'Entero': int,
        'Flotante': float,
        'Bool': bool,
        'Complejo': complex,
        'Cadena': TDA.Cadena,
        'Caracter': TDA.Cadena
    }
    
    target_type = type_conversions.get(datatype_str)
    if target_type is None:
        raise TypeError(f"Tipo básico '{datatype_str}' no soportado")
    
    # Si el valor ya es del tipo correcto, devolverlo
    if isinstance(value, target_type):
        return value
    
    # Intentar conversión según el tipo
    try:
        if datatype_str == 'Entero':
            if isinstance(value, (float, str)):
                return int(value)
            elif isinstance(value, bool):
                return int(value)  # True->1, False->0
            else:
                raise ValueError(f"No se puede convertir {type(value).__name__} a Entero")
                
        elif datatype_str == 'Flotante':
            if isinstance(value, (int, str)):
                return float(value)
            elif isinstance(value, bool):
                return float(value)  # True->1.0, False->0.0
            else:
                raise ValueError(f"No se puede convertir {type(value).__name__} a Flotante")
                
        elif datatype_str == 'Bool':
            if isinstance(value, (int, float)):
                return bool(value)  # 0->False, cualquier otro->True
            elif isinstance(value, str):
                if value.lower() in ['verdadero', 'true', '1']:
                    return True
                elif value.lower() in ['falso', 'false', '0']:
                    return False
                else:
                    raise ValueError(f"String '{value}' no se puede convertir a Bool")
            else:
                raise ValueError(f"No se puede convertir {type(value).__name__} a Bool")
                
        elif datatype_str == 'Complejo':
            if isinstance(value, (int, float)):
                return complex(value)
            elif isinstance(value, str):
                return complex(value)  # Debe estar en formato "1+2j"
            else:
                raise ValueError(f"No se puede convertir {type(value).__name__} a Complejo")
                
        elif datatype_str in ['Cadena', 'Caracter']:
            if isinstance(value, str):
                return TDA.Cadena(value)
            elif hasattr(value, '__str__'):
                return TDA.Cadena(str(value))
            else:
                raise ValueError(f"No se puede convertir {type(value).__name__} a {datatype_str}")
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error convirtiendo valor '{value}' a tipo '{datatype_str}': {str(e)}")

def handle_nested_containers(datatypes: list[str], value) -> TDA.Arreglo | TDA.Conjunto:
    """
    Maneja la creación y población de contenedores anidados (Arreglo/Conjunto).
    
    Args:
        datatypes: Lista de tipos, ej: ["Arreglo", "Arreglo", "Entero"]
        value: Valor a asignar (puede ser lista, objeto TDA existente, etc.)
        
    Returns:
        Instancia del contenedor anidado correspondiente
    """
    if len(datatypes) < 2:
        raise TypeError("Contenedor requiere al menos tipo interno")
    
    tipo_contenedor = datatypes[0]
    
    if tipo_contenedor not in ['Arreglo', 'Conjunto']:
        raise TypeError(f"Tipo contenedor '{tipo_contenedor}' no soportado en esta función")
    
    # Resolver el tipo interno recursivamente
    def resolve_inner_type_for_containers(types_list):
        """Resuelve el tipo para el constructor del contenedor"""
        if len(types_list) == 1:
            # Tipo final - puede ser básico o contenedor
            tipo_final = types_list[0]
            
            # Tipos básicos (tiposa)
            tipos_basicos = {
                'Entero': int,
                'Flotante': float,
                'Bool': bool,
                'Complejo': complex,
                'Cadena': TDA.Cadena,
                'Caracter': TDA.Cadena
            }
            
            if tipo_final in tipos_basicos:
                return tipos_basicos[tipo_final]
            
            # Tipos contenedores (tiposb)
            tipos_contenedores = {
                'Arreglo': TDA.Arreglo,
                'Conjunto': TDA.Conjunto,
                'Diccionario': TDA.Diccionario,
                'Matriz': TDA.Matriz,
                'MatrizRachas': TDA.MatrizRachas,
                'Multicotomizacion': TDA.Multicotomizacion,
                'M2VClasificacion': TDA.M2VClasificacion
            }
            
            if tipo_final in tipos_contenedores:
                return tipos_contenedores[tipo_final]
            
            raise TypeError(f"Tipo '{tipo_final}' no reconocido")
        else:
            # Tipo anidado - devolver la clase contenedora
            if types_list[0] == 'Arreglo':
                return TDA.Arreglo
            elif types_list[0] == 'Conjunto':
                return TDA.Conjunto
            else:
                # Para otros contenedores, también devolver su clase
                tipos_contenedores = {
                    'Diccionario': TDA.Diccionario,
                    'Matriz': TDA.Matriz,
                    'MatrizRachas': TDA.MatrizRachas,
                    'Multicotomizacion': TDA.Multicotomizacion,
                    'M2VClasificacion': TDA.M2VClasificacion
                }
                return tipos_contenedores.get(types_list[0])

    # Obtener el tipo para el constructor
    inner_type = resolve_inner_type_for_containers(datatypes[1:])
    
    # Crear el contenedor principal
    if tipo_contenedor == 'Arreglo':
        new_container = TDA.Arreglo(inner_type)
        
        # Poblar el contenedor según el tipo de value
        if value is None:
            # Contenedor vacío
            pass
        elif isinstance(value, TDA.Arreglo):
            # Ya es un Arreglo - validar que sea compatible
            if value.datatype != inner_type:
                raise ValueError(f"Arreglo existente tiene tipo {value.datatype}, se esperaba {inner_type}")
            new_container = value
        elif isinstance(value, list):
            # Es una lista - poblar elemento por elemento
            for elem in value:
                if len(datatypes) > 2:  # Hay más niveles de anidamiento
                    processed_elem = handle_nested_containers(datatypes[1:], elem)
                else:  # Es el tipo final
                    processed_elem = convert_to_final_type(datatypes[1], elem)
                new_container.pushback(processed_elem)
        else:
            raise ValueError(f"Valor de tipo {type(value).__name__} no compatible con Arreglo")
            
    elif tipo_contenedor == 'Conjunto':
        new_container = TDA.Conjunto(inner_type)
        
        # Poblar el contenedor según el tipo de value
        if value is None:
            # Contenedor vacío
            pass
        elif isinstance(value, TDA.Conjunto):
            # Ya es un Conjunto - validar que sea compatible
            if value.datatype != inner_type:
                raise ValueError(f"Conjunto existente tiene tipo {value.datatype}, se esperaba {inner_type}")
            new_container = value
        elif isinstance(value, list):
            # Es una lista - poblar elemento por elemento
            for elem in value:
                if len(datatypes) > 2:  # Hay más niveles de anidamiento
                    processed_elem = handle_nested_containers(datatypes[1:], elem)
                else:  # Es el tipo final
                    processed_elem = convert_to_final_type(datatypes[1], elem)
                new_container.add(processed_elem)
        else:
            raise ValueError(f"Valor de tipo {type(value).__name__} no compatible con Conjunto")
    
    return new_container

def convert_to_final_type(datatype_str: str, value):
    """
    Convierte un valor al tipo final especificado (puede ser básico o contenedor).
    
    Args:
        datatype_str: String del tipo final
        value: Valor a convertir
        
    Returns:
        Valor convertido al tipo especificado
    """
    # Tipos básicos (tiposa)
    tipos_basicos = ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']
    if datatype_str in tipos_basicos:
        return handle_type_a_conversion(datatype_str, value)
    
    # Tipos contenedores (tiposb) - para casos simples sin anidamiento en este nivel
    elif datatype_str in ['Arreglo', 'Conjunto', 'Diccionario', 'Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion']:
        # Si es un contenedor, debería manejarse en nivel superior
        # Por ahora, asumir que value ya es del tipo correcto
        tipo_map = {
            'Arreglo': TDA.Arreglo,
            'Conjunto': TDA.Conjunto,
            'Diccionario': TDA.Diccionario,
            'Matriz': TDA.Matriz,
            'MatrizRachas': TDA.MatrizRachas,
            'Multicotomizacion': TDA.Multicotomizacion,
            'M2VClasificacion': TDA.M2VClasificacion
        }
        expected_type = tipo_map[datatype_str]
        if not isinstance(value, expected_type):
            raise ValueError(f"Se esperaba {datatype_str}, pero se recibió {type(value).__name__}")
        return value
    
    else:
        raise TypeError(f"Tipo '{datatype_str}' no reconocido")

def handle_special_containers(datatypes: list[str], value):
    """
    Maneja tipos contenedores especiales: Matriz, MatrizRachas, Multicotomizacion, M2VClasificacion, Diccionario.
    
    Args:
        datatypes: Lista de tipos, ej: ["Diccionario", "Cadena", "Entero"] o ["Matriz", "Flotante"]
        value: Valor a validar/convertir
        
    Returns:
        Instancia del tipo contenedor validada/convertida
    """
    if not datatypes:
        raise TypeError("Lista de tipos vacía")
    
    tipo_principal = datatypes[0]
    
    if tipo_principal == 'Diccionario':
        return handle_diccionario_case(datatypes, value)
    elif tipo_principal in ['Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion']:
        return handle_tda_containers_case(datatypes, value)
    else:
        raise TypeError(f"Tipo contenedor especial '{tipo_principal}' no soportado")

def handle_diccionario_case(datatypes: list[str], value) -> TDA.Diccionario:
    """
    Maneja el caso específico de Diccionario con validación y conversión.
    
    Args:
        datatypes: ["Diccionario", "TipoClave", "TipoValor"]
        value: dict de Python o TDA.Diccionario
        
    Returns:
        TDA.Diccionario validado/convertido
    """
    if len(datatypes) < 3:
        raise TypeError("Diccionario requiere tipo de clave y tipo de valor: ['Diccionario', 'TipoClave', 'TipoValor']")
    
    tipo_clave_str = datatypes[1]
    tipo_valor_str = datatypes[2]
    
    # Convertir tipos string a tipos Python
    tipo_clave_py = language_type_to_python_type(tipo_clave_str)
    tipo_valor_py = language_type_to_python_type(tipo_valor_str)
    
    # Manejar según el tipo de value
    if value is None:
        # Crear diccionario vacío
        return TDA.Diccionario(tipo_clave_py, tipo_valor_py)
    
    elif isinstance(value, dict):
        # Convertir dict de Python a TDA.Diccionario
        nuevo_diccionario = TDA.Diccionario(tipo_clave_py, tipo_valor_py)
        
        for key, val in value.items():
            # Convertir clave al tipo correcto
            if tipo_clave_str in ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']:
                converted_key = handle_type_a_conversion(tipo_clave_str, key)
            else:
                # Para tipos contenedores, asumir que ya es del tipo correcto
                if not isinstance(key, tipo_clave_py):
                    raise ValueError(f"Clave {key} no es del tipo esperado {tipo_clave_str}")
                converted_key = key
            
            # Convertir valor al tipo correcto
            if tipo_valor_str in ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']:
                converted_val = handle_type_a_conversion(tipo_valor_str, val)
            else:
                # Para tipos contenedores, asumir que ya es del tipo correcto
                if not isinstance(val, tipo_valor_py):
                    raise ValueError(f"Valor {val} no es del tipo esperado {tipo_valor_str}")
                converted_val = val
            
            nuevo_diccionario[converted_key] = converted_val
        
        return nuevo_diccionario
    
    elif isinstance(value, TDA.Diccionario):
        # Validar que los tipos coincidan
        if value.key_datatype != tipo_clave_py:
            raise ValueError(f"Diccionario tiene tipo de clave {value.key_datatype}, se esperaba {tipo_clave_py}")
        if value.value_datatype != tipo_valor_py:
            raise ValueError(f"Diccionario tiene tipo de valor {value.value_datatype}, se esperaba {tipo_valor_py}")
        
        return value
    
    else:
        raise ValueError(f"Valor de tipo {type(value).__name__} no compatible con Diccionario")

def handle_tda_containers_case(datatypes: list[str], value):
    """
    Maneja casos de contenedores TDA especiales: Matriz, MatrizRachas, Multicotomizacion, M2VClasificacion.
    
    Args:
        datatypes: Lista de tipos, ej: ["Matriz", "Entero"]
        value: Objeto TDA del tipo correspondiente
        
    Returns:
        Objeto TDA validado
    """
    tipo_principal = datatypes[0]
    
    # Mapeo de tipos string a clases TDA
    tipo_classes = {
        'Matriz': TDA.Matriz,
        'MatrizRachas': TDA.MatrizRachas,
        'Multicotomizacion': TDA.Multicotomizacion,
        'M2VClasificacion': TDA.M2VClasificacion
    }
    
    expected_class = tipo_classes.get(tipo_principal)
    if expected_class is None:
        raise TypeError(f"Tipo contenedor TDA '{tipo_principal}' no soportado")
    
    # Validar que value sea del tipo correcto
    if not isinstance(value, expected_class):
        raise ValueError(f"Se esperaba {tipo_principal}, pero se recibió {type(value).__name__}")
    
    # Validaciones específicas por tipo
    if tipo_principal == 'Matriz':
        if len(datatypes) > 1:
            # Validar tipo de datos interno de la matriz
            tipo_interno_str = datatypes[1]
            tipo_interno_py = language_type_to_python_type(tipo_interno_str)
            
            if value.datatype != tipo_interno_py:
                raise ValueError(f"Matriz tiene tipo de dato {value.datatype}, se esperaba {tipo_interno_py}")
    
    elif tipo_principal == 'MatrizRachas':
        # MatrizRachas siempre tiene datatype Cadena
        if hasattr(value, 'datatype') and value.datatype != TDA.Cadena:
            raise ValueError(f"MatrizRachas debe tener datatype Cadena, tiene {value.datatype}")
    
    elif tipo_principal == 'Multicotomizacion':
        if len(datatypes) > 1:
            # Validar tipo de datos interno
            tipo_interno_str = datatypes[1]
            tipo_interno_py = language_type_to_python_type(tipo_interno_str)
            
            if value.datatype != tipo_interno_py:
                raise ValueError(f"Multicotomizacion tiene tipo de dato {value.datatype}, se esperaba {tipo_interno_py}")
    
    elif tipo_principal == 'M2VClasificacion':
        if len(datatypes) > 1:
            # Validar tipo de datos interno
            tipo_interno_str = datatypes[1]
            tipo_interno_py = language_type_to_python_type(tipo_interno_str)
            
            if value.datatype != tipo_interno_py:
                raise ValueError(f"M2VClasificacion tiene tipo de dato {value.datatype}, se esperaba {tipo_interno_py}")
    
    return value

# =============================================================================
# UTILITY FUNCTION FOR ENVIRONMENT VARIABLE LOOKUP
# =============================================================================

def get_variable_from_env(env, variable_id: str):
    """
    Busca una variable en el entorno y retorna su tipo de dato y valor.
    
    Args:
        env: Entorno de ejecución (diccionario con 'data_local' y 'data')
        variable_id: ID de la variable a buscar
        
    Returns:
        tuple: (datatype, value) donde datatype es lista de tipos y value es el valor
        
    Raises:
        ValueError: Si la variable no está definida en el entorno
    """
    # Primero buscar en data_local (variables locales)
    if variable_id in env.get('data_local', {}):
        datatype, value = env['data_local'][variable_id]
        return datatype, value
    
    # Luego buscar en data (variables globales)
    elif variable_id in env.get('data', {}):
        datatype, value = env['data'][variable_id]
        return datatype, value
    
    # Si no se encuentra en ningún lado, lanzar error
    else:
        raise ValueError(f"Variable '{variable_id}' no está definida en el entorno")

def create_variables(variables_dict: dict[str, tuple[list[str], any]], env=None):
    """
    Crea variables en el entorno usando la lógica existente de VariableDeclaration.
    En data_local se guardan las variables locales.
    En data se guardan las variables globales. Pero aun no se implementa.

    Args:
        variables_dict: Diccionario con clave ID (str) y valor (datatype: list[str], value: any)
        env: Entorno de ejecución (opcional, si no se proporciona usa SERVER.env)
        
    Returns:
        dict: Diccionario con los resultados de la creación de variables
            - 'success': Lista de IDs de variables creadas exitosamente
            - 'errors': Lista de tuplas (ID, error) para variables que fallaron
            
    Examples:
        variables = {
            'x': (['Entero'], 42),
            'arr': (['Arreglo', 'Entero'], [1, 2, 3]),
            'mat': (['Matriz', 'Flotante'], None)
        }
        result = crear_variables(variables_dict, env)
    """
    if env is None:
        env = SERVER.env
    
    results = {
        'success': [],
        'errors': []
    }
    
    for variable_id, (datatype, value) in variables_dict.items():
        try:
            # Verificar que la variable no esté ya definida
            if variable_id in env.get('data_local', {}) or variable_id in env.get('data', {}):
                raise ValueError(f"'{variable_id}' ya está definida. No se puede definir variable con el mismo ID (nombre)")
            
            # Usar la misma lógica que VariableDeclaration.eval() para convertir/validar el valor
        # Caso A: Tipo básico (un solo elemento en datatype)
            if len(datatype) == 1:
                tipo_basico = datatype[0]
            # Verificar que sea un tipo básico válido
            tipos_basicos = ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']
            if tipo_basico in tipos_basicos:
                    converted_value = handle_type_a_conversion(tipo_basico, value)
            else:
                raise TypeError(f"Tipo básico '{tipo_basico}' no reconocido")
        
        # Caso B: Tipos contenedores Arreglo/Conjunto (más de un elemento en datatype)
            elif len(datatype) > 1:
                tipo_principal = datatype[0]
            
            if tipo_principal in ['Arreglo', 'Conjunto']:
                # Manejar Arreglos y Conjuntos anidados
                    converted_value = handle_nested_containers(datatype, value)
            elif tipo_principal in ['Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion', 'Diccionario']:
                # Caso C: Manejar contenedores especiales
                    converted_value = handle_special_containers(datatype, value)
            else:
                raise TypeError(f"Tipo contenedor '{tipo_principal}' no implementado")
        
        else:
            raise TypeError("Declaración de tipo vacía o mal formada")

            # Guardar la variable en el entorno local
            if 'data_local' not in env:
                env['data_local'] = {}
            env['data_local'][variable_id] = (datatype, converted_value)
            
            results['success'].append(variable_id)
            
        except Exception as e:
            results['errors'].append((variable_id, str(e)))

    # Si hay errores, lanzar error
    if len(results['errors']) > 0:
        raise ValueError(f"Error al crear variables: {results['errors']}")
    
    return results

def update_variables(variables_dict: dict[str, tuple[list[str], any]], env=None):
    """
    Actualiza variables en el entorno usando la lógica existente de VariableDeclaration.
    En data_local se guardan las variables locales.
    En data se guardan las variables globales. Pero aun no se implementa.

    Args:
        variables_dict: Diccionario con clave ID (str) y valor (datatype: list[str], value: any)
        env: Entorno de ejecución (opcional, si no se proporciona usa SERVER.env)
        
    Returns:
        dict: Diccionario con los resultados de la creación de variables
            - 'success': Lista de IDs de variables creadas exitosamente
            - 'errors': Lista de tuplas (ID, error) para variables que fallaron
            
    Examples:
        variables = {
            'x': (['Entero'], 42),
            'arr': (['Arreglo', 'Entero'], [1, 2, 3]),
            'mat': (['Matriz', 'Flotante'], None)
        }
        result = crear_variables(variables_dict, env)
    """
    if env is None:
        env = SERVER.env
    
    results = {
        'success': [],
        'errors': []
    }
    
    for variable_id, (datatype, value) in variables_dict.items():
        try:
            # Verificar que la variable no esté ya definida
            if not (variable_id in env.get('data_local', {}) or variable_id in env.get('data', {})):
                raise ValueError(f"'{variable_id}' no está definida. No se puede actualizar variable que no existe")
            
            # Usar la misma lógica que VariableDeclaration.eval() para convertir/validar el valor
            # Caso A: Tipo básico (un solo elemento en datatype)
            if len(datatype) == 1:
                tipo_basico = datatype[0]
                # Verificar que sea un tipo básico válido
                tipos_basicos = ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']
                if tipo_basico in tipos_basicos:
                    converted_value = handle_type_a_conversion(tipo_basico, value)
                else:
                    raise TypeError(f"Tipo básico '{tipo_basico}' no reconocido")
            
            # Caso B: Tipos contenedores Arreglo/Conjunto (más de un elemento en datatype)
            elif len(datatype) > 1:
                tipo_principal = datatype[0]
                
                if tipo_principal in ['Arreglo', 'Conjunto']:
                    # Manejar Arreglos y Conjuntos anidados
                    converted_value = handle_nested_containers(datatype, value)
                elif tipo_principal in ['Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion', 'Diccionario']:
                    # Caso C: Manejar contenedores especiales
                    converted_value = handle_special_containers(datatype, value)
                else:
                    raise TypeError(f"Tipo contenedor '{tipo_principal}' no implementado")
            
            else:
                raise TypeError("Declaración de tipo vacía o mal formada")
            
            # Guardar la variable en el entorno local
            env['data_local'][variable_id] = (datatype, converted_value)
            
            results['success'].append(variable_id)
            
        except Exception as e:
            results['errors'].append((variable_id, str(e)))

    # Si hay errores, lanzar error
    if len(results['errors']) > 0:
        raise ValueError(f"Error al crear variables: {results['errors']}")
    
    return results


# =============================================================================

class Server:
    def __init__(self):
        """
        Los nombre de funciones también son clave de env
        Los tipos de datos se guardan como 
        """
        self.env: dict[str, any] = {}
        self.env['data_local']: dict = {} # Las variables son ID: (datatype, value)
        self.env['data']: dict = {} # Las variables son ID: (datatype, value)
        self.env['stack']: list[tuple[str, list, dict]] = [] # Se guarda (func_ID, porgramNodes, data)
        self.env['program_iterator']: list = [] # Se guarda ProgramNode como lista de nodos

    def add_function(self, ID: str, datatypes: list[str], params: dict[str, tuple[list, any]], body: list):
        # Validar que el ID sea un string
        if not isinstance(ID, str):
            raise ValueError("ID de función inválido")
        # Validar que los datatypes sean una lista de strings
        if not isinstance(datatypes, list):
            raise ValueError("Datatypes de función inválidos")
        # Validar que los parámetros que se ve le van a pasar al server sean validos
        for param_id, (datatype, value) in params.items():
            if not isinstance(param_id, str):
                raise ValueError("Parámetro inválido")
            if not isinstance(datatype, list):
                raise ValueError("Tipo de parámetro inválido")
            if not isinstance(value, str):
                raise ValueError("Valor de parámetro inválido")
        # Validar que el body sea una lista de program Nodes
        if not isinstance(body, list):
            raise ValueError("Body de función inválido")

        self.env[ID] = {
            "datatypes": datatypes, # Lista de datatypes
            "params": params, # Diccionario de ID: (datatype, value)
            "body": body, # Lista de program Nodes
        }

    def program_action(self):
        if len(self.env['program_iterator']) > 0:
            statement = self.env['program_iterator'].pop(0)
            statement.eval(self.env)
            self.program_action()
        else:
            self.env['stack'].pop()
            if len(self.env['stack']) > 0:
                func_ID: str = self.env['stack'][-1][0]
                program_nodes: list = self.env['stack'][-1][1]
                data: dict = self.env['stack'][-1][2]
            else:
                raise ValueError("No function to switch to")

            if not func_ID in self.env:
                raise ValueError(f"Function '{func_ID}' not found")

            if program_nodes is not None:
                self.env['program_iterator'].extend(program_nodes)
            else:
                warnings.warn(f"Function '{func_ID}' has no body")
            
            self.env['data_local'] = {}
            if data is not None:
                self.env['data_local'].update(data)

            self.program_action()

    def start_program(self):
        if ('Principal' not in self.env.keys()):
            raise ValueError("Principal function not found")

        create_variables(self.env['Principal']['params'], self.env)
        program_nodes = self.env['Principal']['body']
        self.env['program_iterator'].extend(program_nodes)

        self.env['stack'].append(('Principal', program_nodes, {}))

        self.program_action()

    def swicth_function(self, func_ID: str):
        # Validar que el ID de la función sea un string
        if not isinstance(func_ID, str):
            raise ValueError("ID de función  no es String")

        # Validar que la función exista
        if not func_ID in self.env:
            raise ValueError(f"Function '{func_ID}' not found")
        if len(self.env['stack']) == 0:
            raise ValueError("No function to switch to")

        # En el stack en el espacio de la funcion actual, la previa, se guarde
        #prev_function_ID = self.env['stack'][-1][0]
        self.env['stack'][-1][1] = self.env['program_iterator']
        self.env['stack'][-1][2] = self.env['data_local']

        # Limpias para la nueva función    
        self.env['program_iterator'] = []
        self.env['data_local'] = {}

        # Procesar parámetros de la función, los crea como variables en data_local del env
        create_variables(self.env[func_ID]['params'], self.env)

        self.env['stack'].append((func_ID, None, {}))
        self.env['program_iterator'].extend(self.env[func_ID]['body'])
        

SERVER = Server()

class ProgramNode:
    def __init__(self):
        pass

    def __repr__(self):
        return f"ProgramNode()"

    def eval(self):
        SERVER.start_program()


class MainNode:
    def __init__(self, statements: list):
        self.statements = statements
        SERVER.add_function('Principal', [], {}, self.statements)

    def __repr__(self):
        return f"MainNode(statements={self.statements})"


class FuncNode:
    def __init__(self, datatypes: list[str], ID: str,
                 params: dict[str, tuple[list, any]], body: list):
        self.datatypes = datatypes
        self.ID = ID
        self.params = params
        self.body = body

        # Añade la función al servidor
        SERVER.add_function(ID, datatypes, params, body)

    def __repr__(self):
        return f"FuncNode(datatypes={self.datatypes}, ID={self.ID}, params={self.params}, body={self.body})"


class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

    def eval(self, env):
        """
        Evaluates the expression and prints the result.
        """
        # Si expression tiene metodo eval, evalua, sino imprime literalmente
        if hasattr(self.expression, 'eval'):
            value = self.expression.eval(env)
        else:
            value = self.expression

        print(value)


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
        try:
            value = self.expression.eval(env)
        except AttributeError:
            value = self.expression
            warnings.warn(f"Expression {self.expression} does not have an eval method, using expression directly")

        # Guarda la variable en el entorno, y trata de validar o convertir el value
        variable_dict = {self.ID: (self.datatype, value)}
        create_variables(variable_dict, env)

class GenericVariableDeclNode:
    def __init__(self, datatype: list[str], ID: str, arg_list: list):
        self.datatype = datatype
        self.ID = ID
        self.arg_list = arg_list

    def __repr__(self):
        return f"GenericVariableDeclNode(datatype={self.datatype}, ID={self.ID}, arg_list={self.arg_list})"

    def eval(self, env):
        """
        Evaluates generic variable declarations.
        """
        if self.ID in env['data_local'].keys() or self.ID in env['data'].keys():
            raise ValueError(f"'{self.ID}' already defined. Can't define variable with the same ID (name)")

        # Primer caso: Conjunto o Arreglo (pueden ser anidados)
        if self.datatype[0] in ['Conjunto', 'Arreglo']:
            # Verificar que arg_list esté vacío para este caso
            if self.arg_list:
                raise ValueError(f"Para declaraciones de {self.datatype[0]} anidados, arg_list debe estar vacío")
            
            # Crear contenedor vacío usando la lógica existente
            # Llamamos handle_nested_containers con value=None para crear contenedor vacío
            value = handle_nested_containers(self.datatype, None)
        
        # Segundo caso: Diccionario
        elif self.datatype[0] == 'Diccionario':
            # Verificar que datatype tenga 3 elementos: [Diccionario, TipoClave, TipoValor]
            if len(self.datatype) != 3:
                raise ValueError("Diccionario requiere exactamente 3 tipos: [Diccionario, TipoClave, TipoValor]")
            
            # Verificar que arg_list esté vacío
            if self.arg_list:
                raise ValueError("Para declaraciones de Diccionario, arg_list debe estar vacío")
            
            # Crear diccionario vacío usando la lógica existente
            value = handle_special_containers(self.datatype, None)
        
        # Tercer caso: Matriz
        elif self.datatype[0] == 'Matriz':
            # Verificar que datatype tenga 2 elementos: [Matriz, TipoElemento]
            if len(self.datatype) != 2:
                raise ValueError("Matriz requiere exactamente 2 tipos: [Matriz, TipoElemento]")
            
            # Verificar que arg_list tenga filas y columnas
            if not self.arg_list or len(self.arg_list) != 2:
                raise ValueError("Matriz requiere exactamente 2 argumentos: [filas, columnas]")
            
            filas, columnas = self.arg_list[0], self.arg_list[1]
            
            # Validar que filas y columnas sean enteros positivos
            if not isinstance(filas, int) or filas <= 0:
                raise ValueError(f"Número de filas debe ser un entero positivo, recibido: {filas}")
            if not isinstance(columnas, int) or columnas <= 0:
                raise ValueError(f"Número de columnas debe ser un entero positivo, recibido: {columnas}")
            
            # Obtener el tipo de elemento
            tipo_elemento_str = self.datatype[1]
            tipo_elemento_py = language_type_to_python_type(tipo_elemento_str)
            
            # Crear matriz con dimensiones especificadas
            value = TDA.Matriz(filas, columnas, tipo_elemento_py)
        
        # Cuarto caso: MatrizRachas
        elif self.datatype[0] == 'MatrizRachas':
            # Verificar que datatype tenga 1 elemento: [MatrizRachas]
            if len(self.datatype) != 1:
                raise ValueError("MatrizRachas requiere exactamente 1 tipo: [MatrizRachas]")
            
            # Verificar que arg_list tenga bloques y tratamientos
            if not self.arg_list or len(self.arg_list) != 2:
                raise ValueError("MatrizRachas requiere exactamente 2 argumentos: [bloques, tratamientos]")
            
            bloques, tratamientos = self.arg_list[0], self.arg_list[1]
            
            # Validar que bloques y tratamientos sean válidos
            # Los bloques y tratamientos pueden ser listas o arrays según el constructor de TDA.MatrizRachas
            if bloques is None:
                raise ValueError("Bloques no puede ser None")
            if tratamientos is None:
                raise ValueError("Tratamientos no puede ser None")
            
            # Crear MatrizRachas con bloques y tratamientos especificados
            value = TDA.MatrizRachas(bloques, tratamientos)
        
        # Quinto caso: Multicotomizacion
        elif self.datatype[0] == 'Multicotomizacion':
            # Verificar que datatype tenga 2 elementos: [Multicotomizacion, TipoElemento]
            if len(self.datatype) != 2:
                raise ValueError("Multicotomizacion requiere exactamente 2 tipos: [Multicotomizacion, TipoElemento]")
            
            # Verificar que arg_list tenga solo categorías
            if not self.arg_list or len(self.arg_list) != 1:
                raise ValueError("Multicotomizacion requiere exactamente 1 argumento: [categorias]")
            
            categorias = self.arg_list[0]
            
            # Validar que categorías sea un Conjunto
            if not isinstance(categorias, TDA.Conjunto):
                raise ValueError(f"Categorías debe ser un Conjunto, recibido: {type(categorias).__name__}")
            
            # Obtener el tipo de dato desde datatype[1]
            tipo_dato_str = self.datatype[1]
            tipo_dato_py = language_type_to_python_type(tipo_dato_str)
            
            # Crear Multicotomizacion con categorías y tipo de dato especificados
            value = TDA.Multicotomizacion(categorias, tipo_dato_py)
        
        # Sexto caso: M2VClasificacion
        elif self.datatype[0] == 'M2VClasificacion':
            # Verificar que datatype tenga 2 elementos: [M2VClasificacion, TipoElemento]
            if len(self.datatype) != 2:
                raise ValueError("M2VClasificacion requiere exactamente 2 tipos: [M2VClasificacion, TipoElemento]")
            
            # Verificar que arg_list tenga paramGlobal, bloques y tratamientos
            if not self.arg_list or len(self.arg_list) != 3:
                raise ValueError("M2VClasificacion requiere exactamente 3 argumentos: [paramGlobal, bloques, tratamientos]")
            
            paramGlobal, bloques, tratamientos = self.arg_list[0], self.arg_list[1], self.arg_list[2]
            
            # Validar que bloques sea un Arreglo
            if not isinstance(bloques, TDA.Arreglo):
                raise ValueError(f"Bloques debe ser un Arreglo, recibido: {type(bloques).__name__}")
            
            # Validar que tratamientos sea un Arreglo
            if not isinstance(tratamientos, TDA.Arreglo):
                raise ValueError(f"Tratamientos debe ser un Arreglo, recibido: {type(tratamientos).__name__}")
            
            # Obtener el tipo de dato desde datatype[1]
            tipo_dato_str = self.datatype[1]
            tipo_dato_py = language_type_to_python_type(tipo_dato_str)
            
            # Crear M2VClasificacion con todos los parámetros especificados
            value = TDA.M2VClasificacion(paramGlobal, bloques, tratamientos, tipo_dato_py)
        
        else:
            raise TypeError(f"Tipo '{self.datatype[0]}' no implementado en GenericVariableDeclNode")

        # Guardar en el entorno
        env['data_local'][self.ID] = (self.datatype, value)

class VariableAssignationSimple:
    def __init__(self, ID: str, operator: str, expression):
        self.ID = ID
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return f"VariableAssignationSimple(ID={self.ID}, operator={self.operator}, expression={self.expression})"

    def eval(self, env):
        """
        Evaluates simple variable assignments with support for compound operators.
        """
        # Obtener el tipo de dato y valor actual de la variable existente
        try:
            datatype, current_value = get_variable_from_env(env, self.ID)
        except ValueError:
            raise ValueError(f"'{self.ID}' no definida hasta el momento")
        
        try:
            new_value = self.expression.eval(env)
        except AttributeError:
            new_value = self.expression
            warnings.warn(f"Expression {self.expression} does not have an eval method, using expression directly")
        
        # Verificar si es operador de asignación compuesta
        compound_operators = ['+=', '-=', '*=', '/=', '//=', '%=', '@=', '**=']
        
        if self.operator in compound_operators:
            # Mapear operador compuesto a operador básico
            operator_map = {
                '+=': '+',
                '-=': '-', 
                '*=': '*',
                '/=': '/',
                '//=': '//',
                '%=': '%',
                '@=': '@',
                '**=': '**'
            }
            
            basic_operator = operator_map[self.operator]
            
            # Aplicar la operación entre el valor actual y el nuevo valor
            try:
                if basic_operator == '+':
                    value = current_value + new_value
                elif basic_operator == '-':
                    value = current_value - new_value
                elif basic_operator == '*':
                    value = current_value * new_value
                elif basic_operator == '/':
                    value = current_value / new_value
                elif basic_operator == '//':
                    value = current_value // new_value
                elif basic_operator == '%':
                    value = current_value % new_value
                elif basic_operator == '@':
                    value = current_value @ new_value
                elif basic_operator == '**':
                    value = current_value ** new_value
                else:
                    raise ValueError(f"Operador '{basic_operator}' no soportado")
            except Exception as e:
                raise TypeError(f"No se puede aplicar operador '{basic_operator}' entre {type(current_value)} y {type(new_value)}: {e}")
        
        elif self.operator == '=':
            # Asignación simple
            value = new_value
        else:
            raise ValueError(f"Operador '{self.operator}' no reconocido")
        
        update_variables({self.ID: (datatype, value)}, env)

class VariableAssignationItemAccess:
    def __init__(self, ID: str, item_access: list[int], 
        operator: str, expression):
        self.ID = ID
        self.item_access = item_access
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return f"VariableAssignationItemAccess(ID={self.ID}, item_access={self.item_access}, operator={self.operator}, expression={self.expression})"

    def eval(self, env):
        """
        Evaluates variable assignments with item access (e.g., arr[0] = value, mat[1][2] += 5).
        """
        if self.ID not in env['data_local'].keys() and self.ID not in env['data'].keys():
            raise ValueError(f"'{self.ID}' no definida hasta el momento")
        
        # Obtener el tipo de dato y valor actual de la variable existente
        try:
            datatype, container = get_variable_from_env(env, self.ID)
        except ValueError:
            raise ValueError(f"'{self.ID}' no definida hasta el momento")
        
        # Evaluar la nueva expresión
        try:
            new_value = self.expression.eval(env)
        except AttributeError:
            new_value = self.expression
            warnings.warn(f"Expression {self.expression} does not have an eval method, using expression directly")
        
        # Navegar a través de los índices para obtener el elemento actual
        current_element = container
        
        # Navegar hasta el penúltimo nivel
        for i, index in enumerate(self.item_access[:-1]):
            try:
                if hasattr(current_element, '__getitem__'):
                    current_element = current_element[index]
                else:
                    raise TypeError(f"El objeto en el índice {i} no soporta indexing")
            except (IndexError, KeyError) as e:
                raise IndexError(f"Índice {index} fuera de rango en la posición {i}: {e}")
        
        # Obtener el índice final
        final_index = self.item_access[-1]
        
        # Obtener el valor actual del elemento final
        try:
            if hasattr(current_element, '__getitem__'):
                current_value = current_element[final_index]
            else:
                raise TypeError(f"El objeto no soporta indexing para el índice final {final_index}")
        except (IndexError, KeyError) as e:
            raise IndexError(f"Índice final {final_index} fuera de rango: {e}")
        
        # Verificar si es operador de asignación compuesta
        compound_operators = ['+=', '-=', '*=', '/=', '//=', '%=', '@=', '**=']
        
        if self.operator in compound_operators:
            # Mapear operador compuesto a operador básico
            operator_map = {
                '+=': '+',
                '-=': '-', 
                '*=': '*',
                '/=': '/',
                '//=': '//',
                '%=': '%',
                '@=': '@',
                '**=': '**'
            }
            
            basic_operator = operator_map[self.operator]
            
            # Aplicar la operación entre el valor actual del elemento y el nuevo valor
            try:
                if basic_operator == '+':
                    final_value = current_value + new_value
                elif basic_operator == '-':
                    final_value = current_value - new_value
                elif basic_operator == '*':
                    final_value = current_value * new_value
                elif basic_operator == '/':
                    final_value = current_value / new_value
                elif basic_operator == '//':
                    final_value = current_value // new_value
                elif basic_operator == '%':
                    final_value = current_value % new_value
                elif basic_operator == '@':
                    final_value = current_value @ new_value
                elif basic_operator == '**':
                    final_value = current_value ** new_value
                else:
                    raise ValueError(f"Operador '{basic_operator}' no soportado")
            except Exception as e:
                raise TypeError(f"No se puede aplicar operador '{basic_operator}' entre {type(current_value)} y {type(new_value)}: {e}")
        
        elif self.operator == '=':
            # Asignación simple
            final_value = new_value
        else:
            raise ValueError(f"Operador '{self.operator}' no reconocido")
        
        # Determinar el tipo del elemento para conversión
        # Para elementos de contenedores, necesitamos inferir el tipo basado en el datatype del contenedor
        element_type = self._infer_element_type(datatype, len(self.item_access), container)
        
        # Convertir final_value al tipo correcto del elemento
        if element_type:
            if len(element_type) == 1:
                # Tipo básico
                tipo_basico = element_type[0]
                tipos_basicos = ['Entero', 'Flotante', 'Bool', 'Complejo', 'Cadena', 'Caracter']
                if tipo_basico in tipos_basicos:
                    final_value = handle_type_a_conversion(tipo_basico, final_value)
            elif len(element_type) > 1:
                # Tipo contenedor
                if element_type[0] in ['Arreglo', 'Conjunto']:
                    final_value = handle_nested_containers(element_type, final_value)
                elif element_type[0] in ['Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion', 'Diccionario']:
                    final_value = handle_special_containers(element_type, final_value)
        
        # Actualizar el elemento en el contenedor
        try:
            if hasattr(current_element, '__setitem__'):
                current_element[final_index] = final_value
            else:
                raise TypeError(f"El objeto no soporta asignación por índice")
        except (IndexError, KeyError) as e:
            raise IndexError(f"No se puede asignar al índice {final_index}: {e}")
    
    def _infer_element_type(self, datatype: list[str], access_depth: int, container_obj):
        """
        Infiere el tipo de elemento basado en el datatype del contenedor y la profundidad de acceso.
        """
        if not datatype or access_depth <= 0:
            return None
        
        # Para Arreglo<Tipo> o Conjunto<Tipo>, el elemento es de tipo Tipo
        if datatype[0] in ['Arreglo', 'Conjunto'] and len(datatype) > 1:
            if access_depth == 1:
                # Un solo índice: devolver el tipo interno
                return datatype[1:]
            else:
                # Múltiples índices: recursivo
                return self._infer_element_type(datatype[1:], access_depth - 1, None)
        
        # Para Matriz, el tipo se obtiene del atributo datatype del objeto
        elif datatype[0] == 'Matriz':
            if hasattr(container_obj, 'datatype'):
                matriz_element_type = container_obj.datatype
                # Convertir el tipo Python a lista de tipos del lenguaje (maneja tipos anidados)
                element_type_list = python_type_to_language_type_list(matriz_element_type)
                
                if access_depth == 1:
                    # matriz[i] devuelve una fila (lista de elementos del tipo base)
                    return ['Arreglo'] + element_type_list
                elif access_depth == 2:
                    # matriz[i][j] devuelve un elemento del tipo base
                    return element_type_list
        
        # Para Diccionario, el tipo se obtiene del atributo del objeto
        elif datatype[0] == 'Diccionario':
            if hasattr(container_obj, 'value_datatype'):
                dict_value_type = container_obj.value_datatype
                # Convertir el tipo Python a lista de tipos del lenguaje (maneja tipos anidados)
                value_type_list = python_type_to_language_type_list(dict_value_type)
                
                if access_depth == 1:
                    # dict[key] devuelve el tipo valor
                    return value_type_list
        
        # Para MatrizRachas, similar a Matriz
        elif datatype[0] == 'MatrizRachas':
            # MatrizRachas siempre contiene objetos Cadena (rachas)
            if access_depth == 1:
                return ['Arreglo', 'Cadena']  # fila de rachas
            elif access_depth == 2:
                return ['Cadena']  # una racha individual
        
        # Para otros casos o tipos no reconocidos
        return None

# =============================================================================

class LambdaNode:
    def __init__(self, param_list: list[str], expression):
        """
        Constructor para expresiones lambda.
        
        Args:
            param_list: Lista de nombres de parámetros (IDs)
            expression: Expresión a evaluar cuando se llame la lambda
        """
        self.param_list: list[str] = param_list
        self.expression = expression

    def __repr__(self):
        return f"LambdaNode(param_list={self.param_list}, expression={self.expression})"

    def eval(self, env):
        """
        Evalúa la expresión lambda y retorna una función callable.
        
        Returns:
            function: Función que puede ser llamada con argumentos
        """
        # Capturar el entorno actual para crear un closure
        captured_env = env.copy()
        
        def lambda_function(*args):
            """
            Función lambda generada que puede ser llamada con argumentos.
            
            Args:
                *args: Argumentos pasados a la lambda
                
            Returns:
                Resultado de evaluar la expresión con los parámetros sustituidos
            """
            # Verificar que el número de argumentos coincida con el número de parámetros
            if len(args) != len(self.param_list):
                raise ValueError(f"Lambda esperaba {len(self.param_list)} argumentos, pero recibió {len(args)}")
            
            # Crear un nuevo entorno para la evaluación de la lambda
            lambda_env = captured_env.copy()
            
            # Si no existe data_local, crearlo
            if 'data_local' not in lambda_env:
                lambda_env['data_local'] = {}
            
            # Crear una copia del data_local para no modificar el original
            lambda_env['data_local'] = lambda_env['data_local'].copy()
            
            # Asignar los argumentos a los parámetros en el entorno local
            for param_name, arg_value in zip(self.param_list, args):
                # Inferir el tipo del argumento
                arg_type = self._infer_argument_type(arg_value)
                lambda_env['data_local'][param_name] = (arg_type, arg_value)
            
            # Evaluar la expresión en el entorno con los parámetros asignados
            try:
                if hasattr(self.expression, 'eval'):
                    result = self.expression.eval(lambda_env)
                else:
                    # Si la expresión no tiene método eval, retornarla directamente
                    result = self.expression
                return result
            except Exception as e:
                raise RuntimeError(f"Error evaluando lambda: {e}")
        
        # Agregar metadatos a la función para debugging
        lambda_function.__name__ = f"lambda({', '.join(self.param_list)})"
        lambda_function.__doc__ = f"Lambda function with parameters: {self.param_list}"
        lambda_function.param_list = self.param_list
        lambda_function.expression = self.expression
        
        return lambda_function
    
    def _infer_argument_type(self, value):
        """
        Infiere el tipo del lenguaje basado en el valor del argumento.
        
        Args:
            value: Valor del argumento
            
        Returns:
            list[str]: Lista con el tipo inferido
        """
        # Mapeo de tipos Python a tipos del lenguaje
        if isinstance(value, int):
            return ['Entero']
        elif isinstance(value, float):
            return ['Flotante']
        elif isinstance(value, bool):
            return ['Bool']
        elif isinstance(value, complex):
            return ['Complejo']
        elif isinstance(value, str):
            return ['Cadena']
        elif isinstance(value, TDA.Cadena):
            return ['Cadena']
        elif isinstance(value, TDA.Arreglo):
            # Para Arreglos, usar el tipo interno si está disponible
            if hasattr(value, 'datatype'):
                inner_type = python_type_to_language_type_list(value.datatype)
                return ['Arreglo'] + inner_type
            else:
                return ['Arreglo', 'Entero']  # Default fallback
        elif isinstance(value, TDA.Conjunto):
            # Para Conjuntos, usar el tipo interno si está disponible
            if hasattr(value, 'datatype'):
                inner_type = python_type_to_language_type_list(value.datatype)
                return ['Conjunto'] + inner_type
            else:
                return ['Conjunto', 'Entero']  # Default fallback
        elif isinstance(value, TDA.Diccionario):
            # Para Diccionarios, usar los tipos de clave y valor si están disponibles
            if hasattr(value, 'key_datatype') and hasattr(value, 'value_datatype'):
                key_type = python_type_to_language_type_list(value.key_datatype)
                value_type = python_type_to_language_type_list(value.value_datatype)
                return ['Diccionario'] + key_type + value_type
            else:
                return ['Diccionario', 'Cadena', 'Entero']  # Default fallback
        elif isinstance(value, (TDA.Matriz, TDA.MatrizRachas, TDA.Multicotomizacion, TDA.M2VClasificacion)):
            # Para otros tipos TDA, usar el nombre de la clase
            class_name = value.__class__.__name__
            if hasattr(value, 'datatype'):
                inner_type = python_type_to_language_type_list(value.datatype)
                return [class_name] + inner_type
            else:
                return [class_name]
        else:
            # Para tipos no reconocidos, asumir Entero
            return ['Entero']

class ObjFunctionCall:
    def __init__(self, ID: str, ID_funcion: str, arg_list: list):
        """
        Constructor para llamadas a métodos de objetos.
        
        Args:
            ID: Nombre del objeto en el entorno
            ID_funcion: Nombre del método a llamar
            arg_list: Lista de argumentos para el método
        """
        self.ID = ID
        self.ID_funcion = ID_funcion
        self.arg_list = arg_list

    def __repr__(self):
        return f"ObjFunctionCall(ID={self.ID}, ID_funcion={self.ID_funcion}, arg_list={self.arg_list})"

    def eval(self, env):
        """
        Evalúa la llamada al método del objeto.
        
        Args:
            env: Entorno de ejecución
            
        Returns:
            Resultado de la llamada al método
            
        Raises:
            ValueError: Si el objeto no existe
            AttributeError: Si el método no existe en el objeto
            TypeError: Si los argumentos son inválidos
        """
        # Verificar que el objeto existe en el entorno y obtenerlo
        try:
            datatype, obj_value = get_variable_from_env(env, self.ID)
            # Determinar la fuente para actualizaciones posteriores
            if self.ID in env.get('data_local', {}):
                source = 'data_local'
            else:
                source = 'data'
        except ValueError:
            raise ValueError(f"Objeto '{self.ID}' no está definido en el entorno")
        
        # Validar que el objeto no sea None
        if obj_value is None:
            raise ValueError(f"Objeto '{self.ID}' tiene valor None, no se pueden llamar métodos")
        
        # Evaluar los argumentos de la lista
        evaluated_args = []
        for i, arg in enumerate(self.arg_list):
            try:
                if hasattr(arg, 'eval'):
                    # Es una expresión que necesita evaluación
                    evaluated_arg = arg.eval(env)
                elif callable(arg):
                    # Es una función (como lambda)
                    evaluated_arg = arg
                elif isinstance(arg, str):
                    # Es un ID (identificador de variable), buscar en el entorno
                    datatype, value = get_variable_from_env(env, arg)
                    evaluated_arg = value
                else:
                    # Es un valor literal (int, float, bool, etc.)
                    evaluated_arg = arg
                evaluated_args.append(evaluated_arg)
            except Exception as e:
                raise ValueError(f"Error evaluando argumento {i+1}: {e}")
        
        # Verificar que el método existe en el objeto
        if not hasattr(obj_value, self.ID_funcion):
            available_methods = [method for method in dir(obj_value) if not method.startswith('_')]
            raise AttributeError(f"Objeto '{self.ID}' de tipo {type(obj_value).__name__} no tiene método '{self.ID_funcion}'. "
                               f"Métodos disponibles: {available_methods}")
        
        # Intentar llamar al método directamente con los argumentos evaluados
        try:
            result = getattr(obj_value, self.ID_funcion)(*evaluated_args)
            
            # Manejar métodos que modifican el objeto in-place (como pushback, add, etc.)
            # y retornan None, actualizando el objeto en el entorno
            if result is None and self._is_mutating_method(self.ID_funcion):
                # El método modificó el objeto, actualizar en el entorno
                if source == 'data_local':
                    env['data_local'][self.ID] = (datatype, obj_value)
                else:
                    env['data'][self.ID] = (datatype, obj_value)
                
                # Retornar el objeto para permitir chaining o simplemente None
                return obj_value
            
            return result
            
        except TypeError as e:
            # Error de argumentos (número incorrecto, tipos incorrectos, etc.)
            raise TypeError(f"Error llamando método '{self.ID_funcion}' en objeto '{self.ID}': {e}")
        except AttributeError as e:
            # El método no es callable o no existe (doble verificación)
            raise AttributeError(f"'{self.ID_funcion}' no es un método callable en el objeto '{self.ID}': {e}")
        except Exception as e:
            # Otros errores durante la ejecución del método
            raise RuntimeError(f"Error ejecutando método '{self.ID_funcion}' en objeto '{self.ID}': {e}")
    
    def _is_mutating_method(self, method_name: str) -> bool:
        """
        Determina si un método es mutante (modifica el objeto in-place).
        
        Args:
            method_name: Nombre del método
            
        Returns:
            bool: True si el método modifica el objeto
        """
        # Lista de métodos conocidos que modifican objetos TDA
        mutating_methods = {
            # Métodos de Arreglo
            'pushback', 'pushfront', 'popback', 'popfront', 'insert', 'delete',
            
            # Métodos de Conjunto  
            'add', 'remove',
            
            # Métodos de Diccionario
            'pop', 'clear', 'update', 'setdefault',
            
            # Métodos de Matriz
            'modificar',
            
            # Métodos de MatrizRachas
            'modificaRacha',
            
            # Métodos de Multicotomizacion
            'agnadeRegla', 'eliminarRegla',
            
            # Métodos de M2VClasificacion
            'modificar',
            
            # Métodos generales que suelen ser mutantes
            'append', 'extend', 'sort', 'reverse'
        }
        
        return method_name in mutating_methods
    
    def _validate_argument_types(self, method, args):
        """
        Valida los tipos de argumentos para el método (opcional, para mayor robustez).
        
        Args:
            method: Método a llamar
            args: Argumentos evaluados
            
        Note:
            Esta función podría extenderse para validar tipos específicos
            basándose en anotaciones o documentación de métodos TDA.
        """
        # Esta función podría implementarse para validación adicional
        # Por ahora, delegamos la validación al método mismo
        pass

class FunctionCall:
    def __init__(self, ID_funcion: str, arg_list: list):
        self.ID_funcion = ID_funcion
        self.arg_list = arg_list

    def __repr__(self):
        return f"FunctionCall(ID_funcion={self.ID_funcion}, arg_list={self.arg_list})"

    def eval(self, env):
        """
        Evalúa la llamada a función:
        - Llama a swicth_function del servidor
        - Asigna los valores evaluados de arg_list a los parámetros de la función en data_local
        """
        # 1. Llamar a swicth_function para preparar el entorno de la función
        SERVER.swicth_function(self.ID_funcion)

        # 2. Obtener los parámetros de la función desde el entorno
        params_dict = env[self.ID_funcion]['params']
        param_names = list(params_dict.keys())

        if len(param_names) != len(self.arg_list):
            raise ValueError(f"La función '{self.ID_funcion}' espera {len(param_names)} argumentos, pero se recibieron {len(self.arg_list)}")

        # 3. Asignar los valores evaluados de arg_list a los parámetros en data_local
        for param_name, arg_expr in zip(param_names, self.arg_list):
            # Evaluar el argumento si es necesario
            if hasattr(arg_expr, 'eval'):
                value = arg_expr.eval(env)
            elif callable(arg_expr):
                value = arg_expr
            elif isinstance(arg_expr, str):
                # Buscar el valor en el entorno si es un identificador
                try:
                    _, value = get_variable_from_env(env, arg_expr)
                except Exception:
                    value = arg_expr  # Si no está en el entorno, usar el string literal
            else:
                value = arg_expr

            # Obtener el tipo esperado del parámetro
            datatype, _ = params_dict[param_name]
            # Actualizar en data_local (sobrescribe el valor anterior)
            SERVER.env['data_local'][param_name] = (datatype, value)

        # No retorna nada explícitamente, la ejecución de la función continúa en el servidor


# =============================================================================

class RelExpressionNode:
    def __init__(self, termino1, termino2, oprel: str):
        """
        Nodo AST para expresiones relacionales.
        
        Args:
            termino1: Primer término de la comparación (puede ser valor literal, ID, o expresión)
            termino2: Segundo término de la comparación (puede ser valor literal, ID, o expresión)
            oprel: Operador relacional como string ("<=", ">=", "==", "!=", "<", ">")
        """
        self.termino1 = termino1
        self.termino2 = termino2
        self.oprel = oprel

    def __repr__(self):
        return f"RelExpressionNode(termino1={self.termino1}, termino2={self.termino2}, oprel={self.oprel})"

    def eval(self, env):
        """
        Evalúa la expresión relacional.
        
        Args:
            env: Entorno de ejecución
            
        Returns:
            bool: Resultado de la comparación relacional
            
        Raises:
            ValueError: Si las variables no están definidas
            TypeError: Si los tipos no son comparables
            SyntaxError: Si el operador no es válido
        """
        # Evaluar termino1
        if isinstance(self.termino1, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor1 = get_variable_from_env(env, self.termino1)
        elif hasattr(self.termino1, 'eval'):
            # Es una expresión que necesita evaluación
            valor1 = self.termino1.eval(env)
        else:
            # Es un valor literal
            valor1 = self.termino1
        
        # Evaluar termino2
        if isinstance(self.termino2, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor2 = get_variable_from_env(env, self.termino2)
        elif hasattr(self.termino2, 'eval'):
            # Es una expresión que necesita evaluación
            valor2 = self.termino2.eval(env)
        else:
            # Es un valor literal
            valor2 = self.termino2
        
        # Aplicar el operador relacional específico
        try:
            if self.oprel == '<':
                return valor1 < valor2
            elif self.oprel == '>':
                return valor1 > valor2
            elif self.oprel == '<=':
                return valor1 <= valor2
            elif self.oprel == '>=':
                return valor1 >= valor2
            elif self.oprel == '==':
                return valor1 == valor2
            elif self.oprel == '!=':
                return valor1 != valor2
            else:
                raise SyntaxError(f"Operador relacional '{self.oprel}' no reconocido")
        except Exception as e:
            raise TypeError(f"No se puede aplicar operador '{self.oprel}' entre {type(valor1).__name__} y {type(valor2).__name__}: {e}")


class AritExpressionNode:
    def __init__(self, termino1, termino2, oparit: str):
        """
        Nodo AST para expresiones aritméticas.
        
        Args:
            termino1: Primer término de la operación (puede ser valor literal, ID, o expresión)
            termino2: Segundo término de la operación (puede ser valor literal, ID, o expresión)
            oparit: Operador aritmético como string ("+", "-", "*", "/", "//", "%", "@")
        """
        self.termino1 = termino1
        self.termino2 = termino2
        self.oparit = oparit

    def __repr__(self):
        return f"AritExpressionNode(termino1={self.termino1}, termino2={self.termino2}, oparit={self.oparit})"

    def eval(self, env):
        """
        Evalúa la expresión aritmética.
        
        Args:
            env: Entorno de ejecución
            
        Returns:
            Resultado de la operación aritmética
            
        Raises:
            ValueError: Si las variables no están definidas
            TypeError: Si los tipos no son compatibles para la operación
            SyntaxError: Si el operador no es válido
            ZeroDivisionError: Si hay división por cero
        """
        # Evaluar termino1
        if isinstance(self.termino1, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor1 = get_variable_from_env(env, self.termino1)
        elif hasattr(self.termino1, 'eval'):
            # Es una expresión que necesita evaluación
            valor1 = self.termino1.eval(env)
        else:
            # Es un valor literal
            valor1 = self.termino1
        
        # Evaluar termino2
        if isinstance(self.termino2, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor2 = get_variable_from_env(env, self.termino2)
        elif hasattr(self.termino2, 'eval'):
            # Es una expresión que necesita evaluación
            valor2 = self.termino2.eval(env)
        else:
            # Es un valor literal
            valor2 = self.termino2
        
        # Aplicar el operador aritmético específico
        try:
            if self.oparit == '+':
                return valor1 + valor2
            elif self.oparit == '-':
                return valor1 - valor2
            elif self.oparit == '*':
                return valor1 * valor2
            elif self.oparit == '/':
                if valor2 == 0:
                    raise ZeroDivisionError("División por cero")
                return valor1 / valor2
            elif self.oparit == '//':
                if valor2 == 0:
                    raise ZeroDivisionError("División entera por cero")
                return valor1 // valor2
            elif self.oparit == '%':
                if valor2 == 0:
                    raise ZeroDivisionError("Módulo por cero")
                return valor1 % valor2
            elif self.oparit == '@':
                return valor1 @ valor2
            elif self.oparit == '**':
                return valor1 ** valor2
            else:
                raise SyntaxError(f"Operador aritmético '{self.oparit}' no reconocido")
        except ZeroDivisionError:
            # Re-lanzar errores de división por cero tal como son
            raise
        except Exception as e:
            raise TypeError(f"No se puede aplicar operador '{self.oparit}' entre {type(valor1).__name__} y {type(valor2).__name__}: {e}")


class MinusNode:
    def __init__(self, factor):
        """
        Nodo AST para la negación unaria (operador menos unario).
        
        Args:
            factor: Término a negar (puede ser valor literal, ID, o expresión)
        """
        self.factor = factor

    def __repr__(self):
        return f"MinusNode(factor={self.factor})"

    def eval(self, env):
        """
        Evalúa la negación unaria.
        
        Args:
            env: Entorno de ejecución
            
        Returns:
            Valor negativo del factor
            
        Raises:
            ValueError: Si la variable no está definida
            TypeError: Si el valor no se puede negar
        """
        # Evaluar el factor
        if isinstance(self.factor, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor = get_variable_from_env(env, self.factor)
        elif hasattr(self.factor, 'eval'):
            # Es una expresión que necesita evaluación
            valor = self.factor.eval(env)
        else:
            # Es un valor literal
            valor = self.factor
        
        # Aplicar la negación (multiplicar por -1)
        try:
            return -valor
        except Exception as e:
            raise TypeError(f"No se puede negar el valor de tipo {type(valor).__name__}: {e}")


class LogExpressionNode:
    def __init__(self, termino1, termino2, opLOG: str):
        """
        Nodo AST para expresiones lógicas.
        
        Args:
            termino1: Primer término de la operación lógica (puede ser valor literal, ID, o expresión)
            termino2: Segundo término de la operación lógica (puede ser valor literal, ID, o expresión, o None para operaciones unarias)
            opLOG: Operador lógico como string ("&&", "||", "!")
        """
        self.termino1 = termino1
        self.termino2 = termino2
        self.opLOG = opLOG

    def __repr__(self):
        return f"LogExpressionNode(termino1={self.termino1}, termino2={self.termino2}, opLOG={self.opLOG})"

    def eval(self, env):
        """
        Evalúa la expresión lógica.
        
        Args:
            env: Entorno de ejecución
            
        Returns:
            bool: Resultado de la operación lógica
            
        Raises:
            ValueError: Si las variables no están definidas
            TypeError: Si los valores no se pueden usar en operaciones lógicas
            SyntaxError: Si el operador no es válido
        """
        # Evaluar termino1
        if isinstance(self.termino1, str):
            # Es un ID (identificador de variable), buscar en el entorno
            datatype, valor1 = get_variable_from_env(env, self.termino1)
        elif hasattr(self.termino1, 'eval'):
            # Es una expresión que necesita evaluación
            valor1 = self.termino1.eval(env)
        else:
            # Es un valor literal
            valor1 = self.termino1
        
        # Verificar si es operación unaria (termino2 es None)
        if self.termino2 is None:
            # Operación unaria - negación lógica
            try:
                if self.opLOG == '!':
                    # NOT lógico - negar el valor como booleano
                    return not bool(valor1)
                else:
                    raise SyntaxError(f"Operador lógico unario '{self.opLOG}' no reconocido")
            except Exception as e:
                raise TypeError(f"No se puede aplicar operador lógico unario '{self.opLOG}' a {type(valor1).__name__}: {e}")
        
        else:
            # Operación binaria - evaluar termino2
            if isinstance(self.termino2, str):
                # Es un ID (identificador de variable), buscar en el entorno
                datatype, valor2 = get_variable_from_env(env, self.termino2)
            elif hasattr(self.termino2, 'eval'):
                # Es una expresión que necesita evaluación
                valor2 = self.termino2.eval(env)
            else:
                # Es un valor literal
                valor2 = self.termino2
            
            # Aplicar el operador lógico binario específico
            try:
                if self.opLOG == '&&':
                    # AND lógico - evaluar como booleanos
                    return bool(valor1) and bool(valor2)
                elif self.opLOG == '||':
                    # OR lógico - evaluar como booleanos
                    return bool(valor1) or bool(valor2)
                else:
                    raise SyntaxError(f"Operador lógico binario '{self.opLOG}' no reconocido")
            except Exception as e:
                raise TypeError(f"No se puede aplicar operador lógico '{self.opLOG}' entre {type(valor1).__name__} y {type(valor2).__name__}: {e}")


# =============================================================================

class SelectionNode:
    def __init__(self, cond_blocks: list, else_block):
        """
        cond_blocks: lista de tuplas (cond, block)
        else_block: bloque para el caso 'Entonces' o None
        """
        self.cond_blocks = cond_blocks
        self.else_block = else_block

    def __repr__(self):
        return f"SelectionNode(cond_blocks={self.cond_blocks}, else_block={self.else_block})"

    def eval(self, env):
        """
        Evalúa la estructura de selección:
        - Evalúa cada condición en orden; si alguna es True, ejecuta su bloque y termina.
        - Si ninguna condición es True y hay else_block, ejecuta else_block.
        """
        for cond, block in self.cond_blocks:
            cond_value = cond.eval(env) if hasattr(cond, 'eval') else cond
            if cond_value:
                # Ejecutar el bloque asociado
                if isinstance(block, list):
                    for i, stmt in enumerate(block):
                        env['program_iterator'].insert(i, stmt)
                else:
                    raise SyntaxError("Block is not a list")
                return
        # Si ninguna condición fue verdadera, ejecutar else_block si existe
        if self.else_block is not None:
            if isinstance(self.else_block, list):
                for i, stmt in enumerate(self.else_block):
                    env['program_iterator'].insert(i, stmt)
            else:
                raise SyntaxError("Else block is not a list")

class ForNode:
    def __init__(self, init_decl, condition, update_assign, block):
        self.init_decl = init_decl
        self.condition = condition
        self.update_assign = update_assign
        self.block = block
        self.to_check_condition = False

    def __repr__(self):
        return f"ForNode(init_decl={self.init_decl}, condition={self.condition}, update_assign={self.update_assign}, block={self.block})"

    def eval(self, env):

        if self.to_check_condition:
            return self.check_condition(env)
        
        # Inicialización
        if hasattr(self.init_decl, 'eval'):
            self.init_decl.eval(env)
        else:
            raise SyntaxError("La inicialización del for no es válida")
        
        cond_value = self.condition.eval(env) if hasattr(self.condition, 'eval') else self.condition
        if not cond_value:
            return
        # Ejecutar el bloque
        if isinstance(self.block, list):
            acc = 0
            for i, stmt in enumerate(self.block):
                env['program_iterator'].insert(i, stmt)
                acc = i
            self.to_check_condition = True
            env['program_iterator'].insert(acc + 1, self)
            return
        else:
            raise SyntaxError("El bloque del for no es una lista")

    def check_condition(self, env):
        # Ejecutar la actualización
        if hasattr(self.update_assign, 'eval'):
            self.update_assign.eval(env)

            cond_value = self.condition.eval(env) if hasattr(self.condition, 'eval') else self.condition
            if not cond_value:
                self.to_check_condition = False
                return
            # Ejecutar el bloque
            if isinstance(self.block, list):
                acc = -1
                for i, stmt in enumerate(self.block):
                    env['program_iterator'].insert(i, stmt)
                    acc = i
                self.to_check_condition = True
                if acc > -1:
                    env['program_iterator'].insert(acc + 1, self)
                return
            else:
                raise SyntaxError("El bloque del for no es una lista")

        else:
            raise SyntaxError("La actualización del for no es válida")

class WhileNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
        self.to_check_condition = False

    def __repr__(self):
        return f"WhileNode(condition={self.condition}, block={self.block})"

    def eval(self, env):
        if self.to_check_condition:
            return self.check_condition(env)
        # Primera evaluación de la condición
        cond_value = self.condition.eval(env) if hasattr(self.condition, 'eval') else self.condition
        if not cond_value:
            return
        # Ejecutar el bloque
        if isinstance(self.block, list):
            acc = -1
            for i, stmt in enumerate(self.block):
                env['program_iterator'].insert(i, stmt)
                acc = i
            self.to_check_condition = True
            if acc > -1:
                env['program_iterator'].insert(acc + 1, self)
            return
        else:
            raise SyntaxError("El bloque del while no es una lista")

    def check_condition(self, env):
        cond_value = self.condition.eval(env) if hasattr(self.condition, 'eval') else self.condition
        if not cond_value:
            self.to_check_condition = False
            return
        # Ejecutar el bloque
        if isinstance(self.block, list):
            acc = -1
            for i, stmt in enumerate(self.block):
                env['program_iterator'].insert(i, stmt)
                acc = i
            self.to_check_condition = True
            if acc > -1:
                env['program_iterator'].insert(acc + 1, self)
            return
        else:
            raise SyntaxError("El bloque del while no es una lista")


