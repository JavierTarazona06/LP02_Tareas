import ply.yacc as yacc

import lexer
from lexer import tokens

# Definir la función que corresponde al simbolo inicial
start = "program"

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/', '//', '%', '@'),
    ('right', 'UMINUS', '**')
)


# --------------------------------------
# Definiciones Generales
# --------------------------------------

def p_program(p):
    """
    program : program COMMENT
            | program func_declaration
            | main_declaration
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_main_declaration(p):
    """
    main_declaration : PALABCLAVE (PALABCLAVE|TIPOA|TIPOB) PALABCLAVE '(' ')' block
    """
    if p[1] != 'Func':
        raise SyntaxError("Función debe iniciar con Func")
    if (p[2] not in lexer.tiposa + lexer.tiposb and
            p[2] != 'Vacio'):
        raise SyntaxError(f"Tipo de función inválido: {p[2]}")
    if p[3] != 'Principal':
        raise SyntaxError("Última función debe ser Principal")
    p[0] = ('main', p[2], p[4])


def p_func_declaration(p):
    """
    func_declaration : PALABCLAVE (PALABCLAVE|TIPOA|TIPOB) ID '(' param_list ')' block
    """
    # Verificar que inicie con la palabra clave correcta
    if p[1] != 'Func':
        raise SyntaxError("Función debe iniciar con 'Func'")

    # Verificar que el tipo sea válido
    validos = lexer.tiposa + lexer.tiposb + ['Vacio']
    if p[2] not in validos:
        raise SyntaxError(f"Tipo de función inválido: {p[2]}")

    # Construir el nodo AST
    # Formato: ('func', tipo, nombre, contenido_del_bloque)
    p[0] = ('func', p[2], p[3], p[4])

def param_list(p):
    """
    param_list: param_list ',' param_element
                | param_element
    """

def param_element(p):
    """
    param_element: (TIPOA | TIPOB '<' TIPOA '>') ID
    """

def p_block(p):
    """
    block : '{' statement_list '}'
    """
    p[0] = p[2]


def p_statement_list(p):
    """
    statement_list : statement_list statement
                   | statement
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    """
    statement : COMMENT
              | var_declaration ';'
              | obj_func_call ';'
    """
    p[0] = p[1]


def p_var_declaration(p):
    """
    var_declaration : TIPOA ID '=' expression
                   | TIPOB '<' TIPOA '>' ID '=' expression
                   | TIPOB '<' TIPOA '>' ID '=' TIPOB '<' TIPOA '>' '(' arg_list')'
    """
    if len(p) == 5:
        p[0] = ('var_decl', p[1], p[2], p[4])  # (tipo, nombre, valor)
    else:
        p[0] = ('var_decl_param', p[1], p[3], p[5], p[7])  # (tipo, tipo_param, nombre, valor)


def p_expression(p):
    """
    expression: '{' elements_array '}'
                | '[' elements_array ']'
    """


def p_elements_array(p):
    """
    elements_array: strings_array | bools_array
                |  ints_array | floats_array
    """


def strings_array(p):
    """
    strings_array: strings_array',' string
                | string
    """

def string(p):
    """
    string : CARACTER | CADENA
    """


def bools_array(p):
    """
    bools_array: bools_array',' BOOL
                | BOOL
    """


def ints_array(p):
    """
    ints_array: ints_array','ENTERO
                | ENTERO
    """


def floats_array(p):
    """
    floats_array: floats_array',' float
                | float
    """

def float(p):
    """
    float: REAL |  COMPLEJO
    """

def obj_func_call(p):
    """
    obj_func_call: ID '.' ID '(' arg_list  ')'
    """

def arg_list(p):
    """
    arg_list : arg_list ',' arg_element
            |  arg_element
    """

def arg_element(p):
    """
    arg_element: ID | lambda_expression | string | BOOL | ENTERO | float
    """

def lambda_expression(p):
    """
    lambda_expression: PALABCLAVE  '(' rel_expression ')'
    """
    if p[1] != "Lambda":
        raise SyntaxError("Debe ir una Lambda Expression 'Lambda'")

def rel_expression(p):
    """
    rel_expression : arit_expression OPREL arit_expression
    """

def arit_expression(p):
    """
    arit_expression:
    """

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
