import constants
from utils import NumberConversion as NC

registros: list[list[bool]] = []
PC = 0
SP = 1
IR = 2
ESTADO = 3


def set_up():
    # Creación de registros
    word_null = [False for k in range(constants.WORDS_SIZE_BITS)]
    for i in range(constants.REGISTERS_SIZE):
        registros.append(word_null.copy())

def leer(direccion: int) -> int:
    """
    Devuelve la palabra almacenada en una dirección
    """
    word_lista = registros[direccion]
    decimal_value = NC.binary_list2decimal(word_lista)
    return decimal_value


def escribir(direccion: int, palabra_decimal: int) -> None:
    palabra_binaria = NC.decimal2binary_list(palabra_decimal, fix_bits=64)
    registros[direccion] = palabra_binaria

def fetch():
    # Leer PC
    pc_word_decimal: int = leer(PC)
    escribir(IR, pc_word_decimal)
    escribir(PC, pc_word_decimal + 1)
    return 0

def decode():
    IR_word_decimal: int = leer(IR)
    IR_word_bin: list[bool] = NC.decimal2binary_list(IR_word_decimal)
    opcode = IR_word_bin[0:6]
    registro_destino = IR_word_bin[6:11]
    registro_base = IR_word_bin[11:16]
    memoria = IR_word_bin[16:40]
    extra = IR_word_bin[40:64]