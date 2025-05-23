from typing import Callable

import constants
import utils
from utils import NumberConversion as NC


def set_up():
    ALU.set_up()

def leer_reg(direccion: int, bin = False) -> int|list[bool]:
    """
    Devuelve la palabra almacenada en una dirección
    """
    word_lista = ALU.registros[direccion]
    if bin:
        return word_lista
    decimal_value = NC.binary_list2decimal(word_lista)
    return decimal_value


def escribir_reg(direccion: int, palabra: int|list[bool], bin=False) -> None:
    if not bin:
        palabra = NC.decimal2binary_list(palabra, fix_bits=64)
    ALU.registros[direccion] = palabra

def fetch():
    # Leer PC
    pc_word_decimal: int = leer_reg(ALU.PC)
    escribir_reg(ALU.IR, pc_word_decimal)
    escribir_reg(ALU.PC, pc_word_decimal + 1)
    return 0

def decode():
    IR_word_bin: list[bool] = leer_reg(ALU.IR, bin = True)
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
            break
    else:
        raise ValueError("Invalid Type for instruction. It might be not defined.")


class ALU:
    # Convenciones de registros
    registros: list[list[bool]] = []
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
        word_null = [False for k in range(constants.WORDS_SIZE_BITS)]
        for i in range(constants.REGISTERS_SIZE):
            ALU.registros.append(word_null.copy())

    @staticmethod
    def modify_state(value_result: int|list[bool], bin=False):
        if bin:
            value_bin: list[bool] = value_result
            value_result:int = NC.binary_list2decimal(value_result)
        else:
            value_bin: list[bool] = NC.decimal2binary_list(value_result)

        estado = [False for _ in range(constants.WORDS_SIZE_BITS)]

        if value_result == 0:
            estado[constants.WORDS_SIZE_BITS - ALU.C] = True
        if value_result > 0:
            estado[constants.WORDS_SIZE_BITS - ALU.P] = True
        if value_result < 0:
            estado[constants.WORDS_SIZE_BITS - ALU.N] = True
        if len(value_bin) > 64:
            estado[constants.WORDS_SIZE_BITS - ALU.D] = True

        escribir_reg(ALU.ESTADO, estado, bin=True)

    @staticmethod
    def execute_r(opcode_int: int) -> None:
        r_operations: dict[int, Callable[[], None]] = {
            1: ISA.suma,
            2: ISA.resta,
            3: ISA.mult,
            4: ISA.divi,
            5: ISA.y_bit_bit,
            6: ISA.o_bit_bit,
            7: ISA.xor_bit_bit,
            8: ISA.not_bit_bit,
            9: ISA.comp,
            10: ISA.mueve
        }

        try:
            r_operations[opcode_int]()
        except KeyError:
            raise ValueError(f"Opcode {opcode_int} no definido para "
                             f"instrucciones tipo R.")


class UC:
    # Convenciones de segmentos de instrucción
    OPCODE = 0
    REG_DES = 1
    REG_BAS = 2
    ADDRESS = 3
    EXTRA = 4
    instruction_segmented_bin: list[list[bool]] = None

    @staticmethod
    def decode(word_binary: list[bool]) -> None:
        UC.instruction_segmented_bin = [
            word_binary[0:6],
            word_binary[6:11],
            word_binary[11:16],
            word_binary[16:40],
            word_binary[40:64]
        ]

    @staticmethod
    def get_opcode() -> int:
        return NC.binary_list2decimal(
                UC.instruction_segmented_bin[UC.OPCODE]
            )

    @staticmethod
    def get_reg_des() -> int:
        return NC.binary_list2decimal(
                UC.instruction_segmented_bin[UC.REG_DES]
            )

    @staticmethod
    def get_reg_bas() -> int:
        return NC.binary_list2decimal(
                UC.instruction_segmented_bin[UC.REG_BAS]
            )

    @staticmethod
    def get_address() -> int:
        return NC.binary_list2decimal(
                UC.instruction_segmented_bin[UC.ADDRESS]
            )

    @staticmethod
    def get_extra() -> int:
        return NC.binary_list2decimal(
                UC.instruction_segmented_bin[UC.EXTRA]
            )


class ISA:

    # ------------------
    # Type R
    # ------------------

    @staticmethod
    def suma():
        value:int = leer_reg(UC.get_reg_des()) + leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def resta():
        value:int = leer_reg(UC.get_reg_des()) - leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def mult():
        value:int = leer_reg(UC.get_reg_des()) * leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def divi():
        value:int = leer_reg(UC.get_reg_des()) // leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def y_bit_bit():
        value:int = leer_reg(UC.get_reg_des()) & leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def o_bit_bit():
        value:int = leer_reg(UC.get_reg_des()) | leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def xor_bit_bit():
        value:int = leer_reg(UC.get_reg_des()) ^ leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def not_bit_bit():
        value:int = ~leer_reg(UC.get_reg_des())
        ALU.modify_state(value)
        escribir_reg(UC.get_reg_des(), value)

    @staticmethod
    def comp():
        value:int = leer_reg(UC.get_reg_des()) - leer_reg(UC.get_reg_bas())
        ALU.modify_state(value)

    @staticmethod
    def mueve():
        value:int = leer_reg(UC.get_reg_bas())
        escribir_reg(UC.get_reg_des(), value)
        ALU.modify_state(value)