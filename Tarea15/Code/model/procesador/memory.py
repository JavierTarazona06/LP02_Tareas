import constants
from utils import NumberConversion as NC

array: list[list[int]] = []


def set_up():
    cur_address = [0 for j in range(constants.WORDS_SIZE_BITS)]
    for i in range(constants.MEMORY_SIZE):
        array.append(cur_address.copy())


def leer(direccion: int, mode: str) -> int | list[int]:
    """
    Devuelve la palabra almacenada en una dirección
    mode = ["bit", "natural", "int"]
    """
    word_bin = array[direccion]

    modo_funcion = {
        "bin": lambda: word_bin,
        "natural": lambda: NC.binary_list2natural(word_bin),
        "int": lambda: NC.binary_list2entero(word_bin)
    }

    if mode not in modo_funcion:
        raise ValueError(f"Modo '{mode}' no válido. Opciones: {list(modo_funcion)}")

    return modo_funcion[mode]()


def escribir(direccion: int, palabra: int | list[int], mode: str) -> None:
    """
    mode = ["bit", "natural", "int"]
    """
    modo_funcion = {
        "bin": lambda: palabra.copy(),
        "natural": lambda: NC.natural2binary_list(palabra, fix_bits=constants.WORDS_SIZE_BITS),
        "int": lambda: NC.entero2binary_list(palabra, fix_bits=constants.WORDS_SIZE_BITS)
    }

    if mode not in modo_funcion:
        raise ValueError(f"Modo '{mode}' no válido. Opciones: {list(modo_funcion)}")

    palabra_bin: list[int] = modo_funcion[mode]()
    if len(palabra_bin) != constants.WORDS_SIZE_BITS:
        raise ValueError(f"La palabra no tiene {constants.WORDS_SIZE_BITS} bits.")

    array[direccion] = palabra_bin
