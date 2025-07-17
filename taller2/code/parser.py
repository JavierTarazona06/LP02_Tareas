import ply.yacc as yacc

import ASTInterpreter
import lexer
import ASTInterpreter as Nodes
from lexer import tokens

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
    # p[1] es una lista de comentarios o declaraciones de funciones
    p[0] = Nodes.ProgramNode(p[1] + [p[2]] + p[3])


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


def p_datatype(p):
    """
    datatype : TIPOA
           | TIPOB OPREL datatype OPREL
    """
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


def p_func_declaration(p):
    """
    func_declaration : PALABCLAVE (PALABCLAVE|datatype) ID DELIM param_list DELIM block
    """
    if p[4] != '(' or p[6] != ')':
        raise SyntaxError(f"After {p[3]} you must have (...)")

    # Verificar que inicie con la palabra clave correcta
    if p[1] != 'Func':
        raise SyntaxError("Función debe iniciar con 'Func'")

    # Verificar que el tipo sea válido
    if p[2] is 'Vacio':
        p[2] = [p[2]]

    # Construir el nodo AST
    # Formato: ('func', tipo, nombre, parámetros, contenido_del_bloque)
    p[0] = Nodes.FuncNode(p[2], p[3], p[5], p[7])


def p_param_list(p):
    """
    param_list :
               | param_element
               | param_list DELIM param_element
    """
    if len(p) == 1:
        # Caso sin parámetros: lista vacía
        p[0] = []
    elif len(p) == 2:
        # Un solo parámetro
        p[0] = [p[1]]
    else:
        # Agregamos un nuevo parámetro desde una lista ya existente
        if p[2] != ',':
            raise SyntaxError("Add ',' for separating parameters")
        p[0] = p[1] + [p[3]]


def p_param_element(p):
    """
    param_element : datatype ID
    """
    p[0] = (p[1], p[2])  # (TIPOS Lista, ID)


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
    """
    if len(p) == 2:
        # Es un comentario
        return # No hacemos nada, los comentarios se ignoran
    else:
        if p[2] != ';':
            raise SyntaxError("Use ; at the end of te line")
        # Es una declaración de variable o llamada a función de objeto
        p[0] = p[1]


def p_print(p):
    """
    print : PALABCLAVE DELIM (string | ID | obj_func_call) DELIM
    """
    # Validaciones semánticas
    if p[1] != 'imprimir':
        raise SyntaxError("Print statement must start with 'imprimir'")
    if p[2] != '(' or p[4] != ')':
        raise SyntaxError("Syntax for print: imprimir(string | ID | llamada funcion)")

    p[0] = ASTInterpreter.PrintNode(p[3])  # Crea un nodo AST para la impresión


# TODO Seguir desde aca
def p_var_declaration(p):
    """
    var_declaration : datatype ID OPASI ( expression | iterables | obj_func_call)
                    | TIPOB OPREL TIPOA OPREL ID OPASI TIPOB OPREL TIPOA OPREL DELIM arg_list DELIM
    """
    # Caso 1: tipo simple con expresión
    if len(p) == 5:
        if p[3] != '=':
            raise SyntaxError("Use =")
        p[0] = Nodes.VariableDeclaration(p[1], p[2], p[4])

    # Caso 2: tipo genérico con llamada genérica
    elif len(p) == 14:
        if (p[2] != '<' or p[4] != '>' or p[6] != '=' or p[8] != '<' or p[10] != '>'
                or p[11] != '(' or p[13] != ')'):
            raise SyntaxError("Use: <...> and = <...> and (...)")
        # p = [_, TIPOB, '<', TIPOA, '>', ID, '=', TIPOB, '<', TIPOA, '>', '(', arg_list, ')']
        if p[1] != p[7]:
            raise SyntaxError("TIPOB's deben ser iguales en la declaración")
        if p[3] != p[9]:
            raise SyntaxError("TIPOA's deben ser iguales en la declaración")
        p[0] = Nodes.VariableDeclaration([p[1], p[3]], p[5], p[12])
        p[0] = Nodes.GenericVariableDeclNode([p[1], p[3]], p[5], p[12])
        p[0] = (
            'var_decl_generic_call',
            p[1],  # TIPOB contenedor
            p[3],  # TIPOA interno
            p[5],  # nombre de la variable
            p[7],  # TIPOB función/objeto contenedor
            p[9],  # TIPOA función/objeto interno
            p[12]  # arg_list
        )
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
        # p = [_, index]
        p[0] = ('item_access', [p[2]])

    # Caso 2: acceso a un elemento por índice en una expresión más compleja
    elif len(p) == 5:
        if p[1][0] != 'item_access':
            raise SyntaxError("You must use item access for this operation")
        if p[2] != '[' or p[4] != ']':
            raise SyntaxError("You must use [index] for item access")
        # p = [_, item_access, index]
        p[0] = ('item_access', p[1][1].append(p[3]))


def p_var_assignation(p):
    """
    var_assignation : ID OPASI ( expression | obj_func_call | iterables )
                    | ID item_access OPASI ( expression | obj_func_call | iterables)
                    | ID OPASI TIPOB OPREL TIPOA OPREL DELIM arg_list DELIM
                    | ID item_access OPASI TIPOB OPREL TIPOA OPREL DELIM arg_list DELIM
    """
    # Caso 1: asignación simple
    if len(p) == 4:
        # p = [_, ID, OPASI, expression | obj_func_call | iterables]
        p[0] = ('var_assign_simple', p[1], p[2], p[3])

    # Caso 2: asignación con acceso a elemento
    elif len(p) == 5:
        if p[2][0] != 'item_access':
            raise SyntaxError("Use item access for assignment")
        # p = [_, ID, item_access, OPASI, expression | obj_func_call | iterables]
        p[0] = ('var_assign_item_access', p[1], p[2][1], p[3], p[4])

    # Caso 3: asignación con llamada genérica
    elif len(p) == 10:
        if (p[4] != '<' or p[6] != '>' or
                p[7] != '(' or p[9] != ')'):
            raise SyntaxError("Use:  <...> and (...)")
        # p = [_, ID, OPASI, TIPOB, TIPOA, arg_list]
        p[0] = (
            'var_assign_generic_call',
            p[1],  # nombre de la variable
            p[2],  # OPASI
            p[3],  # TIPOB función/objeto contenedor
            p[5],  # TIPOA función/objeto interno
            p[8]  # arg_list
        )

    elif len(p) == 11:
        if (p[5] != '<' or p[7] != '>' or
                p[8] != '(' or p[10] != ')'):
            raise SyntaxError("Use: <...> and (...)")
        p[0] = (
            'var_assign_generic_item_access',
            p[1],  # nombre de la variable
            p[2][1],  # item_access
            p[3],  # OPASI
            p[4],  # TIPOB función/objeto contenedor
            p[6],  # TIPOA función/objeto interno
            p[9]  # arg_list
        )
    else:
        raise SyntaxError("Var assignation wrongly formed")


def p_iterables(p):
    """
    iterables : OPACC elements_array OPACC
              | DELIM elements_array DELIM
    """
    # Crea una tupla ('iterable', tipo_de_corchete, elementos)
    bracket_type = None
    if p[1] == '{' and p[3] == '}':
        bracket_type = 'set'
    elif p[1] == '[' and p[3] == ']':
        bracket_type = 'list'
    if not bracket_type:
        SyntaxError("Invalid Delimitation for iterable (list, set)")
    p[0] = ('iterable', bracket_type, p[2])


def p_elements_array(p):
    """
    elements_array : strings_array
                      | bools_array
                      | ints_array
                      | floats_array
                      | complex_array
    """
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


def p_string(p):
    """
    string : CARACTER
              | CADENA
    """
    p[0] = Nodes.StringNode(p[1])  # Crea un nodo AST para la cadena o carácter


def p_bools_array(p):
    """bools_array : BOOL
                   | bools_array DELIM BOOL"""
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


def p_obj_func_call(p):
    """
    obj_func_call : ID OPACC ID DELIM arg_list DELIM
    """
    if p[2] != '.' or p[4] != '(' or p[6] != ')':
        raise SyntaxError("You must use . and (...) for function calls")
    # p[1] es el nombre del objeto, p[3] es el método, p[5] es la lista de argumentos
    p[0] = ('func_call', p[1], p[3], p[5])


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


def p_arg_element(p):
    """arg_element : ID
                   | lambda_expression
                   | string
                   | BOOL
                   | number"""
    p[0] = p[1]


def p_id_list(p):
    """
    id_list: ID
            | id_list DELIM ID
    """
    # ID
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[2] != ',':
            raise SyntaxError("Use , for separating identifiers")
        p[0] = p[1] + [p[3]]


def p_lambda_expression(p):
    """
    lambda_expression : PALABCLAVE DELIM id_list DELIM expression DELIM
    """
    if p[2] != '(' or p[4] != ',' or p[6] != ')':
        raise SyntaxError("La expresión lambda debe tener: (id1, id2, ..., expression)")
    if p[1] != 'Lambda':
        raise SyntaxError("La expresión lambda debe tener: 'Lambda'")
    p[0] = ('lambda', p[3], p[5])


def p_expression(p):
    """
    expression: rel_expression
                | arit_expression
                | log_expression
    """
    p[0] = p[1]  # Asignamos la expresión al nodo AST


def p_rel_expression(p):
    """
    rel_expression : rel_term OPREL rel_term
    """
    # p[1]: expresión izquierda, p[2]: operador relacional, p[3]: expresión derecha
    p[0] = ('relop', p[2], p[1], p[3])


def p_rel_term(p):
    """
    rel_term : number
                | string
                | BOOL
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
        p[0] = ('binoparit', p[2], p[1], p[3])


def p_term(p):
    """
    term : factor
            | term OPARIT2 factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # oparit2 es '*', '/', '//', '%', '@'
        p[0] = ('binoparit', p[2], p[1], p[3])


def p_factor(p):
    """factor : base
              | factor OPARIT3 base %prec OPARIT3
              | '-' factor %prec UMINUS"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '-':
        p[0] = ('uminus', p[2])
    else:
        p[0] = ('binoparit', p[1], p[3])


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
        p[0] = ('binoplog', p[2], p[1], p[3])


def p_log_term(p):
    """
    log_term: log_base
                | OPLOG2 log_base %prec OPLOG2
    """
    if len(p) == 2:
        p[0] = p[1]  # caso base: solo un log_base
    else:
        # OPLOG2 es '!'
        p[0] = ('oplogneg', p[1], p[2])  # operador unario de negación lógica


def p_log_base(p):
    """
    log_base : BOOL
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
# Sentencias
# --------------------------------------

# --------------------------------------
# Estructuras de Control
# --------------------------------------


# --------------------------------------
# Expresiones
# --------------------------------------


def p_error(p):
    print("Error sintáctico cerca de", p.value if p else 'EOF')
    # Ignorar tokens hasta encontrar ';'
    while True:
        tok = parser.token()
        if not tok or tok.type == ';' or tok.type == '}':
            break
    parser.errok()  # Restablece el estado de error, para que el parser pueda seguir
    return tok  # Re-inyecta el token ';' como próximo lookahead


# Construir el parser
parser = yacc.yacc(debug=True)

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

"""if __name__ == '__main__':
    import sys
    data = open(sys.argv[1]).read()      # tu archivo fuente
    ast_root = parser.parse(data)        # construye AST
    env = {}                              # entorno vacío
    resultado = ast_root.eval(env)       # ejecutar
    print(resultado)"""
