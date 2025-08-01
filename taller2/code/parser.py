import sys
import pickle

import ply.yacc as yacc

import ASTInterpreter
import lexer
import ASTInterpreter as Nodes
from lexer import tokens
from lexer import lexer as lexer_obj
import TDA

# TODO: Manejar los retornos de las funciones y que puedan estar como var assigantion y en print

# Definir la función que corresponde al simbolo inicial
start = "program"

precedence = (
    ('right', 'UMINUS'),  # negación unaria
    ('right', 'OPARIT3'),  # potencia (**), derecha asociativo
    ('left', 'OPARIT2'),  # *, /, //, %, @
    ('left', 'OPARIT1'),  # +, -
    ('right', 'OPLOG2'),  # logic not (!)
    ('left', 'OPLOG1'),  # &&, ||
)


# --------------------------------------
# Definiciones Generales
# --------------------------------------

def p_program(p):
    """
    program : pre_main main_declaration comments_series
    """
    p[0] = Nodes.ProgramNode()


# Cero o más comentarios o declaraciones de funciones al inicio
def p_pre_main(p):
    """
    pre_main : pre_main func_declaration
             | pre_main COMMENT
             |
    """
    if len(p) == 3:
        if p.slice[2].type == 'COMMENT':
            p[0] = p[1]
        else:
            p[0] = p[1] + [p[2]]
    else:
        p[0] = []


# Solo comentarios al final
def p_comments_series(p):
    """
    comments_series : comments_series COMMENT
                  |
    """
    p[0] = []

def p_main_declaration(p):
    """
    main_declaration : PALABCLAVE PALABCLAVE PALABCLAVE DELIM DELIM block
    """
    if p[4] != '(' or p[5] != ')':
        raise SyntaxError(f"After {p[3]} you must have ()")

    if p[1] != 'Func':
        raise SyntaxError("Función debe iniciar con Func")
    if p[2] != 'Vacio':
        raise SyntaxError(f"Tipo de función inválido: {p[2]}. Tiene que ser 'Vacio'")
    if p[3] != 'Principal':
        raise SyntaxError("Última función debe ser Principal")
    # p = # p = [_, lista de sentencias]
    p[0] = Nodes.MainNode(p[6])


def p_func_type(p):
    """
    func_type : PALABCLAVE
              | datatype
    """
    p[0] = p[1]

def p_func_declaration(p):
    """
    func_declaration : PALABCLAVE func_type ID DELIM param_list DELIM block
    """
    if p[4] != '(' or p[6] != ')':
        raise SyntaxError(f"After {p[3]} you must have (...)")

    # Verificar que inicie con la palabra clave correcta
    if p[1] != 'Func':
        raise SyntaxError("Función debe iniciar con 'Func'")

    # Verificar que el tipo sea válido
    if p[2] == 'Vacio':
        p[2] = []

    p[0] = Nodes.FuncNode(p[2], p[3], p[5], p[7])


def p_param_list(p):
    """
    param_list :
               | param_element
               | param_list DELIM param_element
    """
    if len(p) == 1:
        # Caso sin parámetros: lista vacía
        p[0]: dict[str, tuple[list, any]] = {}
    elif len(p) == 2:
        # Un solo parámetro
        p[0]: dict[str, tuple[list, any]] = p[1]
    else:
        # Agregamos un nuevo parámetro desde una lista ya existente
        if p[2] != ',':
            raise SyntaxError("Add ',' for separating parameters")
        p[0]: dict[str, tuple[list, any]] = p[1]
        p[0].update(p[3])


def p_param_element(p):
    """
    param_element : datatype ID
    """
    p[0]: dict[str, tuple[list, any]] = {str(p[2]): (p[1], None)} # ID:  (TIPOS Lista, valor)


def p_datatype(p):
    """
    datatype : TIPOA
           | TIPOB OPREL datatype OPREL
    """
    p[0]: list[str] = []

    if len(p) == 2:
        # Caso simple: solo un tipo A
        if p[1] not in lexer.tiposa:
            raise SyntaxError(f"Tipo A inválido: {p[1]}")
        p[0] = [str(p[1])]

    elif len(p) == 5:
        # Caso genérico: TIPOB<TIPOA>
        if p[2] != '<' or p[4] != '>':
            raise SyntaxError("Use <...> for generic data type")
        if p[1] not in lexer.tiposb:
            raise SyntaxError(f"Tipo B inválido: {p[1]}")
        p[0] = [str(p[1])] + p[3]

    else:
        raise SyntaxError("Tipo B mal formado")

def p_block(p):
    """
    block : DELIM statement_list DELIM
    """
    if p[1] != '{' or p[3] != '}':
        raise SyntaxError("You have to use {...} for blocks")
    # Asigna el contenido del bloque (lista de sentencias) al nodo AST
    p[0] = p[2]


def p_statement_list(p):
    """
    statement_list : statement
                   | statement_list statement
    """
    if len(p) == 2:
        p[0] = [p[1]]  # una sola sentencia → lista con un elemento
    else:
        p[0] = p[1] + [p[2]]  # agregamos sentencia a la lista existente


def p_statement(p):
    """
    statement : COMMENT
              | var_declaration DELIM
              | var_assignation DELIM
              | obj_func_call DELIM
              | print DELIM
              | func_call DELIM
              | selection_statement DELIM
              | for_statement DELIM
              | while_statement DELIM
    """
    if len(p) == 2:
        # Es un comentario
        return # No hacemos nada, los comentarios se ignoran
    else:
        if p[2] != ';':
            raise SyntaxError("Use ; at the end of te line")
        # Es una declaración de variable o llamada a función de objeto
        p[0] = p[1]


def p_print_content(p):
    """
    print_content : string
                  | ID
                  | obj_func_call
    """
    p[0] = p[1]

def p_print(p):
    """
    print : PALABCLAVE DELIM print_content DELIM
    """
    # Validaciones semánticas
    if p[1] != 'imprimir':
        raise SyntaxError("Print statement must start with 'imprimir'")
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("Syntax for print: imprimir(string | ID | llamada funcion)")

    p[0] = ASTInterpreter.PrintNode(p[3])  # Crea un nodo AST para la impresión


def p_var_decl_value(p):
    """
    var_decl_value : expression
                   | iterables
                   | obj_func_call
                   | boolean
                   | string
    """
    p[0] = p[1]

def p_var_declaration(p):
    """
    var_declaration : datatype ID OPASI var_decl_value
                    | TIPOB OPREL TIPOA OPREL ID OPASI TIPOB OPREL TIPOA OPREL DELIM arg_list DELIM
                    | TIPOB OPREL TIPOA DELIM TIPOB OPREL ID OPASI var_decl_value
    """
    # Caso 1: tipo simple con expresión
    if len(p) == 5:
        if p[3] != '=':
            raise SyntaxError("Use =")
        p[0] = Nodes.VariableDeclaration(p[1], p[2], p[4])

    # Caso 2: Diccionario con tipos específicos
    elif len(p) == 10:
        # Patrón: Diccionario < TipoClave , TipoValor > variable = (obj_func_call | expression)
        if p[1] != 'Diccionario':
            raise SyntaxError("Este patrón solo es válido para Diccionario")
        if p[2] != '<':
            raise SyntaxError("Use < después del tipo Diccionario")
        if p[4] != ',':
            raise SyntaxError("Use , para separar tipos de clave y valor")
        if p[6] != '>':
            raise SyntaxError("Use > para cerrar la declaración de tipos")
        if p[8] != '=':
            raise SyntaxError("Use = para asignación")
        if p[9] == ';':
            p[9] = None
        
        # Construir datatype como [Diccionario, TipoClave, TipoValor]
        datatype = [p[1], p[3], p[5]]
        p[0] = Nodes.VariableDeclaration(datatype, p[7], p[9])

    # Caso 3: tipo genérico con llamada genérica (función constructora)
    elif len(p) == 14:
        if (p[2] != '<' or p[4] != '>' or p[6] != '=' or p[8] != '<' or p[10] != '>'
                or p[11] != '(' or p[13] != ')'):
            raise SyntaxError("Use: <...> and = <...> and (...)")
        # p = [_, TIPOB, '<', TIPOA, '>', ID, '=', TIPOB, '<', TIPOA, '>', '(', arg_list, ')']
        if p[1] != p[7]:
            raise SyntaxError("TIPOB's deben ser iguales en la declaración")
        if p[3] != p[9]:
            raise SyntaxError("TIPOA's deben ser iguales en la declaración")
        
        # Para constructores genéricos, usar GenericVariableDeclNode
        datatype = [p[1], p[3]]
        p[0] = Nodes.GenericVariableDeclNode(datatype, p[5], p[12])
    
    else:
        raise SyntaxError("Declaración de variable mal formada")


def p_item_access(p):
    """
    item_access : OPACC ENTERO OPACC
                | item_access OPACC ENTERO OPACC
    """
    # Caso 1: acceso a un elemento por índice
    if len(p) == 4:
        if p[1] != '[' or p[3] != ']':
            raise SyntaxError("You must use [index] for item access")
        # Guardar lista con un solo índice
        p[0] = [int(p[2])]

    # Caso 2: acceso a un elemento por índice en una expresión más compleja
    elif len(p) == 5:
        if p[2] != '[' or p[4] != ']':
            raise SyntaxError("You must use [index] for item access")
        # Extender la lista existente con el nuevo índice
        p[0] = p[1] + [int(p[3])]


def p_var_assign_value(p):
    """
    var_assign_value : expression
                     | obj_func_call
                     | iterables
                     | string
                     | boolean
    """
    p[0] = p[1]

def p_var_assignation(p):
    """
    var_assignation : ID OPASI var_assign_value
                    | ID item_access OPASI var_assign_value
    """
    # Caso 1: asignación simple
    if len(p) == 4:
        # p = [_, ID, OPASI, expression | obj_func_call | iterables]
        p[0] = Nodes.VariableAssignationSimple(p[1], p[2], p[3])

    # Caso 2: asignación con acceso a elemento
    elif len(p) == 5:
        # p = [_, ID, item_access, OPASI, expression | obj_func_call | iterables]
        p[0] = Nodes.VariableAssignationItemAccess(p[1], p[2], p[3], p[4])

    else:
        raise SyntaxError("Var assignation wrongly formed")


def p_iterables(p):
    """
    iterables : OPACC elements_array OPACC
              | DELIM elements_array DELIM
    """
    # Verificar delimitadores válidos
    bracket_type = None
    if p[1] == '{' and p[3] == '}':
        bracket_type = 'set'
    elif p[1] == '[' and p[3] == ']':
        bracket_type = 'list'
    
    if not bracket_type:
        raise SyntaxError("Invalid Delimitation for iterable (list, set)")
    
    # Verificar que elements_array sea una lista
    if not isinstance(p[2], list):
        raise SyntaxError(f"elements_array debe ser una lista, pero se recibió {type(p[2])}")
    
    # Retornar la lista directamente
    p[0] = list(p[2])

def p_string(p):
    """
    string : CARACTER
              | CADENA
    """
    p[0] = TDA.Cadena(str(p[1]))

def p_boolean(p):
    """
    boolean : BOOL
    """
    if p[1].lower() == "verdadero":
        p[0] = True
    elif p[1].lower() == "falso":
        p[0] = False
    else:
        raise SyntaxError("El valor booleano debe ser verdadero o falso")

def p_number(p):
    """number : ENTERO
              | REAL
              | COMPLEJO"""
    if p.slice[1].type == "ENTERO":
        p[0] = int(p[1])
    elif p.slice[1].type == "REAL":
        p[0] = float(p[1])
    else:
        p[0] = complex(p[1])  # Asumiendo que p[1] es un string tipo '1+2j'

def p_elements_array(p):
    """
    elements_array : strings_array
                      | bools_array
                      | ints_array
                      | floats_array
                      | complex_array
    """
    # Verificar que el resultado sea una lista
    if not isinstance(p[1], list):
        raise SyntaxError(f"elements_array debe producir una lista, pero se recibió {type(p[1])}")
    
    p[0] = p[1]


def p_strings_array(p):
    """
    strings_array : string
                     | strings_array DELIM string
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separation")
        p[0] = p[1] + [p[3]]

def p_bools_array(p):
    """bools_array : boolean
                   | bools_array DELIM boolean"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separation")
        p[0] = p[1] + [p[3]]


def p_ints_array(p):
    """ints_array : ENTERO
                  | ints_array DELIM ENTERO"""
    if len(p) == 2:
        p[0] = [int(p[1])]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separation")
        p[0] = p[1] + [int(p[3])]


def p_floats_array(p):
    """floats_array : REAL
                    | floats_array DELIM REAL"""
    if len(p) == 2:
        p[0] = [float(p[1])]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separation")
        p[0] = p[1] + [float(p[3])]


def p_complex_array(p):
    """complex_array : COMPLEJO
                     | complex_array DELIM COMPLEJO"""
    if len(p) == 2:
        p[0] = [complex(p[1])]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separation")
        p[0] = p[1] + [complex(p[3])]


def p_id_list(p):
    """
    id_list : ID
            | id_list DELIM ID
    """
    # ID
    if len(p) == 2:
        p[0] = [str(p[1])]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separating identifiers")
        p[0] = p[1] + [str(p[3])]

def p_lambda_expression(p):
    """
    lambda_expression : PALABCLAVE DELIM id_list DELIM expression DELIM
    """
    if p[2] != '(' or p[4] != ',' or p[6] != ')':
        raise SyntaxError("La expresión lambda debe tener: (id1, id2, ..., expression)")
    if p[1] != 'Lambda':
        raise SyntaxError("La expresión lambda debe tener: 'Lambda'")
    
    # Crear y retornar un LambdaNode en lugar de una tupla
    # p = [id_list, expression]
    p[0] = Nodes.LambdaNode(p[3], p[5])

def p_arg_element(p):
    """arg_element : ID
                   | lambda_expression
                   | string
                   | boolean
                   | number"""
    p[0] = p[1]

def p_arg_list(p):
    """
    arg_list :
             | arg_element
             | arg_list DELIM arg_element
    """
    if len(p) == 1:
        # No hay argumentos: lista vacía
        p[0] = []
    elif len(p) == 2:
        # Un solo elemento
        p[0] = [p[1]]
    else:
        # vararg_list , arg_element
        if p[2] != ',':
            raise SyntaxError("Use ',' for separating arguments")
        p[0] = p[1] + [p[3]]


def p_obj_func_call(p):
    """
    obj_func_call : ID OPACC ID DELIM arg_list DELIM
    """
    if p[2] != '.' or p[4] != '(' or p[6] != ')':
        raise SyntaxError("You must use . and (...) for function calls")
    
    # Crear y retornar un ObjFunctionCall en lugar de una tupla
    # p = [_, ID, ID, arg_list]
    p[0] = Nodes.ObjFunctionCall(p[1], p[3], p[5])

def p_func_call(p):
    """
    func_call : ID DELIM arg_list DELIM
    """
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("You must use . and (...) for function calls")
    
    p[0] = Nodes.FunctionCall(p[1], p[3])


# --------------------------------------
# Expresiones
# --------------------------------------

def p_expression(p):
    """
    expression : rel_expression
                | arit_expression
                | log_expression
    """
    p[0] = p[1]  # Asignamos la expresión al nodo AST


def p_rel_expression(p):
    """
    rel_expression : rel_term OPREL rel_term
    """
    # Crear y retornar un RelExpressionNode en lugar de evaluar directamente
    p[0] = Nodes.RelExpressionNode(p[1], p[3], p[2])


def p_rel_term(p):
    """
    rel_term : number
                | string
                | boolean
                | ID
                | DELIM expression DELIM
    """
    if len(p) == 4:
        # 'expression' entre paréntesis
        if p[1] != '(' or p[3] != ')':
            raise SyntaxError("You must use ( expression )")
        # p[2] es la expresión dentro de los paréntesis
        p[0] = p[2]
    else:
        # number, string, BOOL o ID
        p[0] = p[1]


def p_arit_expression(p):
    """
    arit_expression : term
                       | arit_expression OPARIT1 term
    """
    if len(p) == 2:
        p[0] = p[1]  # caso base: solo un term
    else:
        # oparit1 es '+', '-'
        p[0] = Nodes.AritExpressionNode(p[1], p[3], p[2])


def p_term(p):
    """
    term : factor
            | term OPARIT2 factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # oparit2 es '*', '/', '//', '%', '@'
        p[0] = Nodes.AritExpressionNode(p[1], p[3], p[2])


def p_factor(p):
    """factor : base
              | factor OPARIT3 base %prec OPARIT3
              | '-' factor %prec UMINUS"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '-':
        p[0] = Nodes.MinusNode(p[2])
    else:
        # **
        p[0] = Nodes.AritExpressionNode(p[1], p[3], p[2])


def p_base(p):
    """
    base : number
        | ID
        | DELIM arit_expression DELIM
    """
    if len(p) == 4:
        if p[1] != '(' or p[3] != ')':
            raise SyntaxError("You must use ( arit_expression )")
        # Caso '( arit_expression )' → extraemos la expresión
        p[0] = p[2]
    else:
        # Caso número o identificador
        p[0] = p[1]


def p_log_expression(p):
    """
    log_expression : log_term
                   | log_expression OPLOG1 log_term
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # OPLOG1 es '&&', '||'
        p[0] = Nodes.LogExpressionNode(p[1], p[3], p[2])


def p_log_term(p):
    """
    log_term : log_base
                | OPLOG2 log_base %prec OPLOG2
    """
    if len(p) == 2:
        p[0] = p[1]  # caso base: solo un log_base
    else:
        # OPLOG2 es '!'
        p[0] = Nodes.LogExpressionNode(p[1], None, p[2])


def p_log_base(p):
    """
    log_base : boolean
              | ID
              | DELIM log_expression DELIM
    """
    if len(p) == 4:
        if p[1] != '(' or p[3] != ')':
            raise SyntaxError("You must use ( log_expression )")
        # Caso '( log_expression )' → extraemos la expresión
        p[0] = p[2]
    else:
        # Caso BOOL o ID
        p[0] = p[1]


# --------------------------------------
# Estructura de seleccion
# --------------------------------------

def p_selection_statement(p):
    """
    selection_statement : si_branch sino_branches entonces_branch_opt
    """
    # p[1] = lista de (cond, block) para Si y Sinos
    # p[2] = lista de (cond, block) para Sinos
    # p[3] = block para Entonces o None
    # Se puede crear un nodo AST tipo SelectionNode(cond_blocks, else_block)
    cond_blocks = p[1] + p[2]  # lista de (cond, block)
    else_block = p[3]  # puede ser None
    p[0] = Nodes.SelectionNode(cond_blocks, else_block)


def p_si_branch(p):
    """
    si_branch : PALABCLAVE DELIM selection_condition DELIM block
    """
    if p[1] != 'Si':
        raise SyntaxError("La estructura de selección debe iniciar con 'Si'")
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("Se espera (condición) después de 'Si'")
    # p[3] es la condición, p[5] es el bloque
    p[0] = [(p[3], p[5])]


def p_sino_branches(p):
    """
    sino_branches : sino_branches sino_branch
                  |
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


def p_sino_branch(p):
    """
    sino_branch : PALABCLAVE DELIM selection_condition DELIM block
    """
    if p[1] != 'Sino':
        raise SyntaxError("Se espera 'Sino'")
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("Se espera (condición) después de 'Sino'")
    p[0] = (p[3], p[5])


def p_entonces_branch_opt(p):
    """
    entonces_branch_opt : PALABCLAVE block
                        |
    """
    if len(p) == 1:
        p[0] = None
    else:
        if p[1] != 'Entonces':
            raise SyntaxError("Se espera 'Entonces'")
        p[0] = p[2]


def p_selection_condition(p):
    """
    selection_condition : log_expression
                        | rel_expression
    """
    p[0] = p[1]

# --------------------------------------
# Estructuras de iteración
# --------------------------------------

def p_for_statement(p):
    """
    for_statement : PALABCLAVE DELIM var_declaration DELIM rel_expression DELIM var_assignation DELIM block
    """
    if p[1] != 'Para':
        raise SyntaxError("La estructura de iteración debe iniciar con 'Para'")
    if p[2] != '(' or p[4] != ';' or p[6] != ';' or p[8] != ')':
        raise SyntaxError("Sintaxis esperada: Para (var_declaration ; rel_expression ; var_assignation) block")
    # p[3]: var_declaration, p[5]: rel_expression, p[7]: var_assignation, p[9]: block
    p[0] = Nodes.ForNode(p[3], p[5], p[7], p[9])

def p_while_statement(p):
    """
    while_statement : PALABCLAVE DELIM rel_expression DELIM block
    """
    if p[1] != 'Mientras':
        raise SyntaxError("La estructura de iteración debe iniciar con 'Mientras'")
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("Sintaxis esperada: Mientras (rel_expression) block")
    # p[3]: rel_expression, p[5]: block
    p[0] = Nodes.WhileNode(p[3], p[5])


# ------------------------------------------------------------------------------
# Errores
# ------------------------------------------------------------------------------

def p_error(p):
    if not p:
        print("Error sintáctico cerca de EOF")
        return
    print("Error sintáctico cerca de", p.value)
    # Ignorar tokens hasta encontrar ';' o '}'
    while True:
        tok = parser.token()
        if not tok or tok.type == ';' or tok.type == '}':
            break
    parser.errok()


# Construir el parser
parser = yacc.yacc(debug=True)

if __name__ == '__main__':
    # Obtener el archivo fuente
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        # Archivo por defecto si no se especifica
        source_file = 'tests/prototype1.txt'
    
    try:
        data = open(source_file).read()      # tu archivo fuente
        print(f"Parseando archivo: {source_file}")
        ast_root = parser.parse(data, lexer = lexer_obj)        # construye AST

        # Guardar el AST
        with open('ast_guardado.pickle', 'wb') as f:
            pickle.dump(ast_root, f)
        print("AST guardado en 'ast_guardado.pickle'")

        if ast_root is not None:
            print("Ejecutando AST...")
            ast_root.eval()
            print("Ejecución completada")
        else:
            raise SyntaxError("Error sintáctico cerca de EOF")
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{source_file}'")
        print("Uso: python parser.py [archivo_fuente]")
    except Exception as e:
        print(f"Error: {e}")

"""
if __name__ == '__main__':
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
"""