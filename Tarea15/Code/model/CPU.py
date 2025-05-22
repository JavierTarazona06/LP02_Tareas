import constants

registros = []
PC = 0
SP = 1
IR = 2
ESTADO = 3

def set_up():

    # Creación de registros
    word_null = [0 for k in range(constants.WORDS_SIZE_BITS)]
    for i in range(constants.REGISTERS_SIZE):
        registros.append(word_null.copy())