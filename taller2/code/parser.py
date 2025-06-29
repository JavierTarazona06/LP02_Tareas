import ply.yacc as yacc
from lexer import tokens

# Definir la función que corresponde al simbolo inicial
start = None


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --------------------------------------
# Definición Global
# --------------------------------------

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
    print("Error de sintaxis")

# Construir el parser
parser = yacc.yacc()

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