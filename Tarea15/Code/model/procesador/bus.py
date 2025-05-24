from typing import Callable

import constants
from model.procesador import memory
from utils import NumberConversion as NC


def set_up():
    Datos.set_up()
    Direccion.set_up()
    Control.set_up()


def action():
    # Lee la instrucción de control y ejecuta su acción respectiva
    instruction: int = Control.leer(bin=False)
    call_instruccion(instruction)


def call_instruccion(instr: int):
    c_operations: dict[int, Callable[[], None]] = {
        Control.LEER_MEMORIA: Control.Instructions.leer_memoria,
        Control.ESCRIBIR_MEMORIA: Control.Instructions.escribir_memoria
    }

    try:
        c_operations[instr]()
    except KeyError:
        raise ValueError(f"Código {instr} no definido para "
                         f"instrucciones de control.")


class Datos:
    array: list[int] = None

    @staticmethod
    def set_up():
        Datos.array = [0 for _ in range(constants.WORDS_SIZE_BITS)]

    @staticmethod
    def leer(mode: str) -> int | list[int]:
        """
        Devuelve la palabra almacenada en el bus de datos
        mode = ["bin","natural","int"]
        """
        word_bin = Datos.array.copy()

        modo_funcion = {
            "bin": lambda: word_bin,
            "natural": lambda: NC.binary_list2natural(word_bin),
            "int": lambda: NC.binary_list2entero(word_bin)
        }

        if mode not in modo_funcion:
            raise ValueError(f"Modo '{mode}' no válido. Opciones: {list(modo_funcion)}")

        return modo_funcion[mode]()

    @staticmethod
    def escribir(palabra: int | list[int], bin=False) -> None:
        if not bin:
            palabra = NC.entero2binary_list(palabra, fix_bits=constants.WORDS_SIZE_BITS)
        else:
            if len(palabra) != constants.WORDS_SIZE_BITS:
                raise ValueError(f"La palabra debe ser de {constants.WORDS_SIZE_BITS} bits")
        Datos.array = palabra.copy()


class Direccion:
    array: list[int] = None

    @staticmethod
    def set_up():
        Direccion.array = [0 for _ in range(constants.MEMORY_BITS)]

    @staticmethod
    def leer(bin=False) -> int | list[int]:
        """
        Devuelve la dirección almacenada en el bus de dirección
        """
        addr_bin: list[int] = Direccion.array
        if bin:
            return addr_bin.copy()
        decimal_value = NC.binary_list2natural(addr_bin)
        return decimal_value

    @staticmethod
    def escribir(direccion: int | list[int], bin=False) -> None:
        if not bin:
            addr = NC.natural2binary_list(direccion, fix_bits=constants.MEMORY_BITS)
        else:
            if len(direccion) != constants.MEMORY_BITS:
                raise ValueError(
                    f"El tamaño de la dirección es "
                    f"diferente al esperado: {constants.MEMORY_BITS}")
            else:
                addr = direccion
        Direccion.array = addr.copy()


class Control:
    array: list[int] = None
    LEER_MEMORIA = 1
    ESCRIBIR_MEMORIA = 2

    @staticmethod
    def set_up():
        Control.array = [0 for _ in range(constants.CONTROL_SIZE)]

    @staticmethod
    def leer(bin=False) -> int | list[int]:
        """
        Devuelve la instrucción de control almacenada en el bus de control
        """
        ctrl_bin: list[int] = Control.array
        if bin:
            return ctrl_bin.copy()
        decimal_value = NC.binary_list2natural(ctrl_bin)
        return decimal_value

    @staticmethod
    def escribir(ctrl: int | list[int], bin=False) -> None:
        if not bin:
            ctrl_i = NC.natural2binary_list(ctrl, fix_bits=constants.CONTROL_SIZE)
        else:
            if len(ctrl) != constants.CONTROL_SIZE:
                raise ValueError(
                    f"El tamaño de la instrucción de control "
                    f"es diferente al esperado: {constants.CONTROL_SIZE}")
            else:
                ctrl_i = ctrl
        Control.array = ctrl_i.copy()

    class Instructions:
        @staticmethod
        def leer_memoria():
            word_bin: list[int] = memory.leer(
                Direccion.leer(bin=False),
                mode="bin"
            )
            Datos.escribir(word_bin, bin=True)

        @staticmethod
        def escribir_memoria():
            word_bin = Datos.leer(mode="bin")
            memory.escribir(
                Direccion.leer(bin=False),
                word_bin,
                mode="bin"
            )
