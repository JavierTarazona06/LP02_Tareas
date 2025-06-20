import ply.lex as lex

# 1. Lista de tokens
tokens = (
    'NUMBER','PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
)



# 2. Reglas regex simples



# 3. Ejecuciones por tipo





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
        s = input('calc> ')
        if not s:
            break
        lexer.input(s)
        for tok in lexer:
            print(tok)
