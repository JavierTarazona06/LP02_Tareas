import ply.lex as lex

# 1. Lista de tokens
tokens = (
    'NUMBER','PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
)

# 2. Reglas regex simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# 3. Número (entero o flotante)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# 4. Ignorar espacios y tabulaciones
t_ignore = ' \t'

# 5. Error
def t_error(t):
    print(f"Error: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# 6. Construir lexer
lexer = lex.lex()

if __name__ == "__main__":
    while True:
        s = input('term> ')
        if not s:
            break
        lexer.input(s)
        for tok in lexer:
            print(tok)
