from typing import Callable

import constants
from utils import NumberConversion as NC

from model.procesador import bus


def set_up():
    ALU.set_up()


def leer_reg(direccion: int, mode: str) -> int | list[int]:
    palabra_bin = ALU.registros[direccion]

    modo_funcion = {
        "bin": lambda: palabra_bin,
        "natural": lambda: NC.binary_list2natural(palabra_bin),
        "int": lambda: NC.binary_list2entero(palabra_bin)
    }

    if mode not in modo_funcion:
        raise ValueError(f"Modo '{mode}' no válido. Opciones: {list(modo_funcion)}")

    return modo_funcion[mode]()


def escribir_reg(direccion: int, palabra: int | list[int], mode: str) -> None:
    modo_funcion = {
        "bin": lambda: palabra.copy(),
        "natural": lambda: NC.natural2binary_list(palabra, fix_bits=constants.WORDS_SIZE_BITS),
        "int": lambda: NC.entero2binary_list(palabra, fix_bits=constants.WORDS_SIZE_BITS)
    }

    if mode not in modo_funcion:
        raise ValueError(f"Modo '{mode}' no válido. Opciones: {list(modo_funcion)}")

    palabra_bin = modo_funcion[mode]()

    if len(palabra_bin) != constants.WORDS_SIZE_BITS:
        raise ValueError(
            f"La palabra debe tener {constants.WORDS_SIZE_BITS} bits.")

    ALU.registros[direccion] = palabra_bin


def fetch():
    # Leer PC
    pc_word_natural = leer_reg(ALU.PC, mode="natural")

    # Traer instrucción a la que apunta el PC
    bus.Control.escribir(bus.Control.LEER_MEMORIA)
    bus.Direccion.escribir(pc_word_natural, bin=False)
    bus.action()
    instruction_bin = bus.Datos.leer(mode="bin")

    # Guardar instrucción en la ALU
    escribir_reg(ALU.IR, instruction_bin, mode="bin")

    # Incrementar PC
    if pc_word_natural == constants.CODE_RANGE[1]:
        pc_word_natural = 0
    else:
        pc_word_natural += 1

    # Guardar PC incrementado
    escribir_reg(ALU.PC, pc_word_natural, mode="natural")
    return 0


def decode():
    IR_word_bin: list[int] = leer_reg(ALU.IR, mode="bin")
    UC.decode(IR_word_bin)


def execute():
    """
    args son los valores que acompañan a la instrucción
    """
    # Verificar tipo
    opcode_int = UC.get_opcode()

    for tipo, (inicio, fin) in {
        "R": constants.INS_TYPE_R,
        "I": constants.INS_TYPE_I,
        "J": constants.INS_TYPE_J
    }.items():
        if inicio <= opcode_int <= fin:
            if tipo == "R":
                ALU.execute_r(opcode_int)
            elif tipo == "I":
                ALU.execute_i(opcode_int)
            break
    else:
        raise ValueError("Invalid Type for instruction. It might be not defined.")


class ALU:
    # Convenciones de registros
    registros: list[list[int]] = []
    PC = 0
    SP = 1
    IR = 2
    ESTADO = 3

    # Flags
    C = 0
    P = 1
    N = 2
    D = 3

    @staticmethod
    def set_up():
        # Creación de registros
        word_null = [0 for k in range(constants.WORDS_SIZE_BITS)]
        for i in range(constants.REGISTERS_SIZE):
            ALU.registros.append(word_null.copy())

    @staticmethod
    def modify_state(value_result: int | list[int], mode: str):
        """
        mode = ["bin", "int"]
        """
        value_bin: list[int] = []

        if mode == "bin":
            value_bin = value_result.copy()
            value_result: int = NC.binary_list2entero(value_result)
        elif mode == "int":
            value_bin: list[int] = NC.entero2binary_list(value_result)

        estado = [0 for _ in range(constants.WORDS_SIZE_BITS)]

        if value_result == 0:
            estado[constants.WORDS_SIZE_BITS - ALU.C] = 1
        if value_result > 0:
            estado[constants.WORDS_SIZE_BITS - ALU.P] = 1
        if value_result < 0:
            estado[constants.WORDS_SIZE_BITS - ALU.N] = 1
        if len(value_bin) > 64:
            estado[constants.WORDS_SIZE_BITS - ALU.D] = 1

        escribir_reg(ALU.ESTADO, estado, mode="bin")

    @staticmethod
    def execute_r(opcode_int: int) -> None:
        r_operations: dict[int, Callable[[], None]] = {
            1: ISA.R.suma,
            2: ISA.R.resta,
            3: ISA.R.mult,
            4: ISA.R.divi,
            5: ISA.R.y_bit_bit,
            6: ISA.R.o_bit_bit,
            7: ISA.R.xor_bit_bit,
            8: ISA.R.not_bit_bit,
            9: ISA.R.comp,
            10: ISA.R.mueve,
            11: ISA.R.limpia,
            12: ISA.R.incr
        }

        try:
            r_operations[opcode_int]()
        except KeyError:
            raise ValueError(f"Opcode {opcode_int} no definido para "
                             f"instrucciones tipo R.")

    @staticmethod
    def execute_i(opcode_int: int) -> None:
        i_operations: dict[int, Callable[[], None]] = {
            13: ISA.I_.cargar,
            14: ISA.I_.guardar,
            15: ISA.I_.carga_inm,
            16: ISA.I_.suma_inm
        }

        try:
            i_operations[opcode_int]()
        except KeyError:
            raise ValueError(f"Opcode {opcode_int} no definido para "
                             f"instrucciones tipo I.")


class UC:
    # Convenciones de segmentos de instrucción
    OPCODE = 0
    REG_DES = 1
    REG_BAS = 2
    ADDRESS = 3
    EXTRA = 4
    instruction_segmented_bin: list[list[int]] = None

    @staticmethod
    def decode(word_binary: list[int]) -> None:
        if len(word_binary) != constants.WORDS_SIZE_BITS:
            raise ValueError(f"Instruction must be of 64 bits")
        UC.instruction_segmented_bin = [
            word_binary[0:6],
            word_binary[6:11],
            word_binary[11:16],
            word_binary[16:40],
            word_binary[40:64]
        ]
        # TODO
        # SI el registro destino o base esta entre 0 y 3, mande error. Porque son los registros reservados

    @staticmethod
    def get_opcode() -> int:
        return NC.binary_list2natural(
            UC.instruction_segmented_bin[UC.OPCODE]
        )

    @staticmethod
    def get_reg_des() -> int:
        return NC.binary_list2entero(
            UC.instruction_segmented_bin[UC.REG_DES]
        )

    @staticmethod
    def get_reg_bas() -> int:
        return NC.binary_list2entero(
            UC.instruction_segmented_bin[UC.REG_BAS]
        )

    @staticmethod
    def get_address() -> int:
        return NC.binary_list2natural(
            UC.instruction_segmented_bin[UC.ADDRESS]
        )

    @staticmethod
    def get_extra() -> int:
        return NC.binary_list2entero(
            UC.instruction_segmented_bin[UC.EXTRA]
        )


class ISA:
    # ------------------
    # Type R
    # ------------------

    class R:
        @staticmethod
        def suma():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") +
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def resta():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") -
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def mult():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") *
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def divi():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") //
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def y_bit_bit():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") &
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def o_bit_bit():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") |
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def xor_bit_bit():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") ^
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def not_bit_bit():
            value: int = ~ (
                leer_reg(UC.get_reg_des(), mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def comp():
            value: int = (
                    leer_reg(UC.get_reg_des(), mode="int") -
                    leer_reg(UC.get_reg_bas(), mode="int")
            )
            ALU.modify_state(value, mode="int")

        @staticmethod
        def mueve():
            value: int = leer_reg(UC.get_reg_bas(), mode="int")
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

        @staticmethod
        def limpia():
            escribir_reg(UC.get_reg_des(), 0, mode="int")

        @staticmethod
        def incr():
            value: int = leer_reg(UC.get_reg_des(), mode="int") + 1
            ALU.modify_state(value, mode="int")
            escribir_reg(UC.get_reg_des(), value, mode="int")

    # ------------------
    # Type I
    # ------------------

    class I_:

        @staticmethod
        def cargar():
            bus.Direccion.escribir(UC.get_address())
            bus.Control.escribir(bus.Control.LEER_MEMORIA)
            bus.action()
            word_bin = bus.Datos.leer(mode="bin")
            escribir_reg(UC.get_reg_des(), word_bin, mode="bin")

        @staticmethod
        def guardar():
            word_bin: list[int] = leer_reg(UC.get_reg_des(), mode="bin")
            bus.Datos.escribir(word_bin, bin=True)
            bus.Direccion.escribir(UC.get_address())
            bus.Control.escribir(bus.Control.ESCRIBIR_MEMORIA)
            bus.action()

        # TODO: Funciona si se hace doble carga para tener un valor mas grande?
        @staticmethod
        def carga_inm():
            """
            Entero
            """
            escribir_reg(
                UC.get_reg_des(),
                UC.get_extra(),
                mode="int"
            )

        @staticmethod
        def suma_inm():
            """
            Entero
            """
            v1 = leer_reg(UC.get_reg_des(), mode="int")
            v2 = UC.get_extra()
            value_result:int = v1 + v2

            escribir_reg(
                UC.get_reg_des(),
                value_result,
                mode="int"
            )

    # ------------------
    # Type J
    # ------------------
