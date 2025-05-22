import utils
import constants

array = []


def set_up():
    cur_address = [0 for j in range(constants.WORDS_SIZE_BITS)]
    for i in range(constants.MEMORY_SIZE):
        array.append(cur_address.copy())


def leer(direccion: int) -> int:
    """
    Devuelve la palabra almacenada en una dirección
    """
    word_lista = array[direccion]
    decimal_value = utils.binary_list2decimal(word_lista)
    return decimal_value


def escribir(direccion: int, palabra_decimal: int) -> None:
    palabra_binaria = utils.decimal2binary_list(palabra_decimal, fix_bits=64)
    array[direccion] = palabra_binaria
