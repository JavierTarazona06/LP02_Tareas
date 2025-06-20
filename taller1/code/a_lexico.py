import ply.lex as lex

# 1. Lista de tokens
tokens = ()

# ------------------------------------
# ------------------------------------

# 3-4. Reglas regex simples -  Ejecuciones por tipo


# -------------------------------
#   PALABCLAVE
# ------------------------------


# -------------------------------
#   TIPO
# ------------------------------


# -------------------------------
#   ID
# ------------------------------



# -------------------------------
#   LITERAL
# ------------------------------



# -------------------------------
#   OPERADOR
# ------------------------------



# -------------------------------
#   DELIM
# ------------------------------





# -------------------------------
#   COMMENT
# ------------------------------




# ------------------------------------
# ------------------------------------

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
