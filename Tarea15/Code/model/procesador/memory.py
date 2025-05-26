import constants
from utils import NumberConversion as NC

import numpy as np

array: list[list[int]] = []


class Memory:
    """
    Clase que representa la memoria del procesador.
    Almacena un array de palabras de tamaño WORDS_SIZE_BITS.
    Cada palabra es una lista de bits (0 o 1).
    La memoria tiene un tamaño de MEMORY_SIZE palabras.
    """
    array: np.ndarray = None

    @staticmethod
    def set_up():
        """
        Inicializa la memoria con un array de ceros.
        Cada palabra tiene WORDS_SIZE_BITS bits.
        La memoria tiene MEMORY_SIZE palabras.
        """
        Memory.array = np.zeros(
            (constants.MEMORY_SIZE, constants.WORDS_SIZE_BITS), dtype=np.uint64)

    @staticmethod
    def read(direction: np.uint64) -> np.uint64:
        """
        Devuelve la palabra almacenada en una dirección.
        :param direction: Dirección de memoria a leer.
        :return: Palabra almacenada en la dirección.
        """
        return Memory.array[direction]

    @staticmethod
    def write(direction: np.uint64, word: np.uint64) -> None:
        """
        Escribe una palabra en una dirección de memoria.
        :param direction: Dirección de memoria a escribir.
        :param word: Palabra a escribir en la dirección.
        """
        if len(word) != constants.WORDS_SIZE_BITS:
            raise ValueError(
                f"La palabra debe tener {constants.WORDS_SIZE_BITS} bits.")
        Memory.array[direction] = word
