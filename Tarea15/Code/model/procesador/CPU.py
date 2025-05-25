from typing import Callable

import constants
import utils
from utils import NumberConversion as NC

from model.procesador import bus

EN_EJECUCION = False

def set_up():
    ALU.set_up()


def leer_reg(direccion: int, mode: str) -> int | list[int]:
    """
    Devuelve contenido del registro en la dirección especificado
    Y lo devuelve según el mode
    mode = ["bin","natural","int"]
    """
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
    """
    Escribe en el registro de la dirección especificada
    la palabra según el mode.
    mode= ["bin","natural","int"]
    """
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
    instruction_bin: list[int] = bus.Datos.leer(mode="bin")

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
    try:
        operations[UC.opcode_length][UC.opcode_offset]()
    except KeyError:
        raise ValueError(f"Instrucción {UC.instruction_asm} no definida.")


def check_register_notspecial(register_num: list[int] | int, bin=True, msg: str = None):
    if bin:
        register_num = NC.binary_list2natural(register_num)
    if 0 <= register_num <= 3:
        if msg:
            raise ValueError(msg)
        raise ValueError(
            "Los registros PC, SP, IR y ESTADO no se pueden modificar con"
            "instrucciones."
        )


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


class UC:
    # Convenciones de segmentos de instrucción
    instruction_word: list[int] = None
    opcode_length: int = None
    opcode_offset: int = None
    instruction_asm: str = None
    instruction_args: list[list[int]] = None

    @staticmethod
    def decode(word_binary: list[int]) -> None:
        if len(word_binary) != constants.WORDS_SIZE_BITS:
            raise ValueError(f"Instruction must be of 64 bits")
        UC.instruction_word = word_binary

        # Encontrar de qué tipo es la instrucción y cuál es
        opcodes_dict = utils.FileManager.JSON2dict(constants.OPCODES_PATH)
        length, offset = None, None
        instr_str = NC.binary_list2str(UC.instruction_word)

        for length_i, opcodes_list in opcodes_dict.items():
            for idx, opcode in enumerate(opcodes_list):
                if instr_str.startswith(opcode):
                    length = length_i
                    offset = idx
                    break
            if length is not None:
                break  # Salir del ciclo exterior si ya se encontró

        if length is None:
            raise ValueError("No existe opcode con el que inicie la instrucción.")
        UC.opcode_length = length
        UC.opcode_offset = offset

        # Obtener la instrucción exacta
        instr_asm_dict = utils.FileManager.JSON2dict(constants.ISA_PATH)
        UC.instruction_asm = instr_asm_dict[UC.opcode_length][UC.opcode_offset]

        # Extract args depending on length type
        UC.instruction_args = []
        if length == 64:
            UC.instruction_args.append(UC.instruction_word)  # Code instruction
        elif length == 54:
            UC.instruction_args.append(UC.instruction_word[0:54])  # Opcode
            UC.instruction_args.append(UC.instruction_word[54:59])  # R
            UC.instruction_args.append(UC.instruction_word[59:64])  # R'
        elif length == 59:
            UC.instruction_args.append(UC.instruction_word[0:59])  # Opcode
            UC.instruction_args.append(UC.instruction_word[59:64])  # R
        elif length == 35:
            UC.instruction_args.append(UC.instruction_word[0:35])  # Opcode
            UC.instruction_args.append(UC.instruction_word[35:40])  # R
            UC.instruction_args.append(UC.instruction_word[40:64])  # M
        elif length == 27:
            UC.instruction_args.append(UC.instruction_word[0:27])  # Opcode
            UC.instruction_args.append(UC.instruction_word[27:32])  # R
            UC.instruction_args.append(UC.instruction_word[32:64])  # V
        elif length == 40:
            UC.instruction_args.append(UC.instruction_word[0:40])  # Opcode
            UC.instruction_args.append(UC.instruction_word[40:64])  # M


class ISA:
    # ------------------
    # Type R
    # ------------------

    class R:
        @staticmethod
        def suma():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") +
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def resta():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") -
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def mult():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") *
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def divi():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") //
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def y_bit_bit():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") &
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def o_bit_bit():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") |
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def xor_bit_bit():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") ^
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def comp():
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = (
                    leer_reg(r, mode="int") -
                    leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")

        @staticmethod
        def copia():
            """
            Mueve de registro base a destino
            """
            r = NC.binary_list2natural(UC.instruction_args[1])
            r_p = NC.binary_list2natural(UC.instruction_args[2])
            value: int = leer_reg(r_p, mode="int")
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def not_bit_bit():
            r = NC.binary_list2natural(UC.instruction_args[1])
            value: int = ~ leer_reg(r, mode="int")
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def limpia():
            r = NC.binary_list2natural(UC.instruction_args[1])
            ALU.modify_state(0, mode="int")
            escribir_reg(r, 0, mode="int")

        @staticmethod
        def incr():
            r = NC.binary_list2natural(UC.instruction_args[1])
            value: int = leer_reg(r, mode="int") + 1
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def decr():
            r = NC.binary_list2natural(UC.instruction_args[1])
            value: int = leer_reg(r, mode="int") - 1
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

    # ------------------
    # Type I
    # ------------------

    class I_:

        @staticmethod
        def cargar():
            """
            Contenido dirección de memoria a registro
            """
            r = NC.binary_list2natural(UC.instruction_args[1])
            m = NC.binary_list2natural(UC.instruction_args[2])

            bus.Direccion.escribir(m)
            bus.Control.escribir(bus.Control.LEER_MEMORIA)
            bus.action()
            word_bin: list[int] = bus.Datos.leer(mode="bin")

            ALU.modify_state(word_bin, mode="bin")

            escribir_reg(r, word_bin, mode="bin")

        @staticmethod
        def guardar():
            """
            Contenido de un registro en una dirección de memoria
            """
            r = NC.binary_list2natural(UC.instruction_args[1])
            m = NC.binary_list2natural(UC.instruction_args[2])

            word_bin: list[int] = leer_reg(r, mode="bin")
            bus.Datos.escribir(word_bin, bin=True)
            bus.Direccion.escribir(m)
            bus.Control.escribir(bus.Control.ESCRIBIR_MEMORIA)
            bus.action()

            ALU.modify_state(word_bin, mode="bin")

        @staticmethod
        def carga_inm():
            """
            Cargar un entero inmediato (32 bits) al registro en
            los bits menos significativos.
            Hace una limpieza antes de cargar para dejarlo como nuevo.
            """
            r = NC.binary_list2natural(UC.instruction_args[1])
            v: list[int] = UC.instruction_args[2]

            # val_rec: list[int] = leer_reg(r, mode="bin")
            val_rec: list[int] = [0 for _ in range(constants.WORDS_SIZE_BITS)]
            val_rec[32:] = v.copy()

            escribir_reg(
                r,
                val_rec,
                mode="bin"
            )
            ALU.modify_state(val_rec, mode="bin")

        @staticmethod
        def carga_inm_superior():
            """
            Cargar un entero inmediato (32 bits) al registro en
            los bits más significativos
            """
            r:int = NC.binary_list2natural(UC.instruction_args[1])
            v: list[int] = UC.instruction_args[2]

            # Leer lo que ya hay
            val_rec: list[int] = leer_reg(r, mode="bin")
            val_rec[0:32] = v.copy()

            escribir_reg(
                r,
                val_rec,
                mode="bin"
            )
            ALU.modify_state(val_rec, mode="bin")

        @staticmethod
        def suma_inm():
            """
            Suma el registro destino con un entero inmediato
            """
            r: int = NC.binary_list2natural(UC.instruction_args[1])
            v: int = NC.binary_list2natural(UC.instruction_args[2])

            v1 = leer_reg(r, mode="int")
            v2 = v
            value_result: int = v1 + v2

            ALU.modify_state(value_result, mode="int")

            escribir_reg(
                r,
                value_result,
                mode="int"
            )

    # ------------------
    # Type J
    # ------------------



operations:dict[int, list[Callable[[], None]]] = {
  64: [
    "PROCRASTINA", "VUELVE", "PARA"
  ],
  54: [
    ISA.R.suma, ISA.R.resta, ISA.R.mult, ISA.R.divi, ISA.R.y_bit_bit,
    ISA.R.o_bit_bit, ISA.R.xor_bit_bit, ISA.R.comp, ISA.R.copia
  ],
  59: [
    ISA.R.not_bit_bit, ISA.R.limpia, ISA.R.incr, ISA.R.decr, "APILA", "DESAPILA"
  ],
  35: [
    ISA.I_.cargar, ISA.I_.guardar, "SIREGCERO", "SIREGNCERO"
  ],
  27: [
    ISA.I_.carga_inm, ISA.I_.carga_inm_superior, ISA.I_.suma_inm, "IRESTA", "IMULT",
    "IDIVI", "IAND", "IOR", "IXOR", "ICOMP"
  ],
  40: [
    "SALTA", "LLAMA", "SICERO", "SINCERO", "SIPOS", "SINEG",
    "SIOVERFL", "SIMAYOR", "SIMENOR", "INTERRUP"
  ]
}