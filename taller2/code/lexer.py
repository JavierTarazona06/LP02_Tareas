import re
import ply.lex as lex

# Lista de literales
#literals = ['+', '-', '*', '/', '(', ')', '{', '}',
#            '<', '>', '=']  # Define caracteres literales

# Lista de tokens
tokens = []

# -------------------------------
#   PALABCLAVE
# ------------------------------

tokens.append('PALABCLAVE')

palabras_reservadas = [
    'Func', 'Principal', 'imprimir', 'Vacio', 'Retornar',
    'Romper', 'Continuar', 'Pasar', 'Sino',
    'Si', 'Entonces', 'Para', 'Mientras', 'Lanzar', 'Intentar',
    'Excepto', 'Lambda'
]
reserved = {w: 'PALABCLAVE' for w in palabras_reservadas}

# -------------------------------
#   TIPO
# ------------------------------

tokens += ['TIPOA', 'TIPOB']

tiposa = ['Bool', 'Entero', 'Flotante', 'Complejo', 'Cadena', 'Caracter']
reserved.update({w: 'TIPOA' for w in tiposa})

tiposb = ['Conjunto', 'Arreglo', 'Matriz', 'MatrizRachas', 'Multicotomizacion', 'M2VClasificacion', 'Diccionario']
'''for t in tiposa:
    tiposb.append(f'Conjunto<{t}>')
    tiposb.append(f'Arreglo<{t}>')
    tiposb.append(f'Matriz<{t}>')
    tiposb.append(f'MatrizRachas<{t}>')
    tiposb.append(f'Multicotomizacion<{t}>')
    tiposb.append(f'M2VClasificacion<{t}>')
    tiposb.append(f'Diccionario<{t},{t}>')'''
reserved.update({w: 'TIPOB' for w in tiposb})

#TIPOB_PATTERN = '|'.join(re.escape(s) for s in tiposb)
#TIPOB_PATTERN = fr'(?:{TIPOB_PATTERN})'

'''def t_TIPOB(t):
    t.type = 'TIPOB'
    return t
t_TIPOB.__doc__ = TIPOB_PATTERN'''

# -------------------------------
#   Caracter y Cadenas
# ------------------------------

tokens += ['CARACTER', 'CADENA']

t_CARACTER = r"'(?:\\.|[^\\'])'"

CADENA_S = r'"(?:\\.|[^"\\])*"'
CADENA_F = (
    r'f"(?:'
    r'\\.'
    r'|[^"\\{]'
    r'|\{[A-Za-z_ñÑ][A-Za-z0-9_ñÑ]*\}'
    r')*"'
)
CADENA_PATTERN = rf'(?:{CADENA_S}|{CADENA_F})'


def t_CADENA(t):
    return t


t_CADENA.__doc__ = CADENA_PATTERN

# -------------------------------
#   ID
# ------------------------------

tokens += ['ID', 'BOOL']

reserved.update({b: 'BOOL' for b in ['Verdadero', 'Falso']})


def t_ID(t):
    r'[A-Za-z_ñÑ][A-Za-z0-9_ñÑ]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# -------------------------------
#   LITERAL
# ------------------------------

tokens += ['ENTERO', 'REAL', 'COMPLEJO']

DIGITO = r'[0-9]'
NATURAL = rf'(?:[1-9]{DIGITO}*|0)'
ENTERO_PATTERN = rf'(?:-?{NATURAL})'
REAL_U = rf'(?:{NATURAL}?\.{NATURAL})(?:[eE][+-]?{NATURAL})?'
REAL_PATTERN = rf'(?:-?{REAL_U})'
COMPLEJO_PATTERN = rf'(?:{REAL_PATTERN}[+-]{REAL_U}[jJ]|{REAL_PATTERN}[jJ])'


def t_COMPLEJO(t):
    t.value = complex(t.value.replace('J', 'j'))
    return t


t_COMPLEJO.__doc__ = COMPLEJO_PATTERN


def t_REAL(t):
    t.value = float(t.value)
    return t


t_REAL.__doc__ = REAL_PATTERN


def t_ENTERO(t):
    t.value = int(t.value)
    return t


t_ENTERO.__doc__ = ENTERO_PATTERN

# -------------------------------
#   COMMENT
# ------------------------------

tokens += ["COMMENT"]

LINEA = r'//[^\n]*'
BLOQUECO = r'/\*[\s\S]*?\*/'
COMMENT_PATTERN = rf'(?:{LINEA}|{BLOQUECO})'


def t_COMMENT(t):
    return t


t_COMMENT.__doc__ = COMMENT_PATTERN

# -------------------------------
#   OPERADOR
# ------------------------------

tokens += ['OPREL', 'OPASI', 'OPASIU', 'OPACC',
           'OPARIT3', 'OPARIT2', 'OPARIT1',
           'OPLOG2', 'OPLOG1']

OPREL_PATTERN = r'(?:<=|>=|==|!=|<|>)'  # <= >= == != < >
OPASI_PATTERN = r'(?:\*\*=|//=|\+=|-=|\*=|/=|%=|@=|=)'  # **= //= += -= *= /= %= @=
OPASIU_PATTERN = r'(?:\+\+|--)'  # ++ --
OPACC_PATTERN = r'[\[\]\.]'  # [ ] .
OPARIT_PATTERN3 = r'(?:\*\*)'  # **
OPARIT_PATTERN2 = r'(?://|\*|/|%|@)'  # // * / % @
OPARIT_PATTERN1 = r'(?:\+|\-)'  # + -
OPLOG_PATTERN2 = r'(?:!)'  # !
OPLOG_PATTERN1 = r'(?:&&|\|\|)'  # && ||


def t_OPREL(t):
    return t


t_OPREL.__doc__ = OPREL_PATTERN


def t_OPASI(t):
    return t


t_OPASI.__doc__ = OPASI_PATTERN


def t_OPASIU(t):
    return t


t_OPASIU.__doc__ = OPASIU_PATTERN


def t_OPACC(t):
    return t


t_OPACC.__doc__ = OPACC_PATTERN


def t_OPARIT3(t):
    return t


t_OPARIT3.__doc__ = OPARIT_PATTERN3


def t_OPARIT2(t):
    return t


t_OPARIT2.__doc__ = OPARIT_PATTERN2


def t_OPARIT1(t):
    return t


t_OPARIT1.__doc__ = OPARIT_PATTERN1


def t_OPLOG2(t):
    return t


t_OPLOG2.__doc__ = OPLOG_PATTERN2

def t_OPLOG1(t):
    return t


t_OPLOG1.__doc__ = OPLOG_PATTERN1

# -------------------------------
#   DELIM
# ------------------------------

tokens += ["DELIM"]

t_DELIM = r'[;{},()]'

# ------------------------------------
# ------------------------------------

# Espacios y Saltos de Línea
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


#tokens = tuple(tokens)

# Error
def t_error(t):
    print(f"Error: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)


# Construir lexer
# Regex legible, ignora espacios en blanco
lexer = lex.lex(reflags=lex.re.VERBOSE)

if __name__ == "__main__":

    while True:
        s = input('term> ')
        ultm_dot = s.rfind('.')

        if not s:
            break

        try:
            with open(s, 'r', encoding='utf-8') as f:
                datos = f.read()

            lexer.input(datos)

            with open(s[:ultm_dot] + '_lex.txt', 'w', encoding='utf-8') as fout:
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    # tok.type es el nombre del token, tok.value su lexema,
                    # tok.lineno y tok.lexpos la línea y posición
                    fout.write(f"{tok.lineno}:{tok.lexpos}\t{tok.type}\t{tok.value}\n")
        except FileNotFoundError:
            print(f"No se encontró el archivo: {s}")

    '''while True:
        s = input('calc> ')
        if not s:
            break
        lexer.input(s)
        for tok in lexer:
            print(tok)'''
