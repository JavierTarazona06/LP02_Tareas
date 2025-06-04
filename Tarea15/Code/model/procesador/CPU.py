import inspect
import numpy as np
from typing import Callable
from bitarray import bitarray

import utils
import constants

from model.procesador import bus
from utils import NumberConversion as NC

# -----------------------
# Public Global Variables
# -----------------------

EN_EJECUCION: bool = False
PARA_INSTRUCTION: bool = False


# -----------------------
# Methods
# -----------------------

def refresh():
    """
    Limpia el entorno
    indicando que ya mo esta en
    ejecución y que no hay una instrucción de parada
    :return:
    """
    global EN_EJECUCION, PARA_INSTRUCTION
    EN_EJECUCION = False
    PARA_INSTRUCTION = False


def preparate(address: int):
    """
    Prepara el entorno de ejecución para el ciclo
    fetch-decode-execute desde
    :param address
    """
    ALU.write_register(ALU.PC, NC.natural2bitarray(address, 64))


def fetch():
    """
    Lee la siguiente instrucción de memoria y la guarda en el registro IR.
    Incrementa el PC para apuntar a la siguiente instrucción.
    """
    # Leer PC para ver a qué palabra apunta
    curr_pc_word_dir: bitarray = ALU.read_register(ALU.PC).copy()
    curr_pc_word_dir = NC.truncate_bitarray_ls(curr_pc_word_dir, 24)

    # Indicarle al bus de control que lea memoria
    bus.ControlBus.write(bus.ControlBus.READ_MEMORY_BIN)

    # Escribir PC en el bus de dirección
    bus.DirectionBus.write(curr_pc_word_dir)

    # Leer la palabra de memoria
    bus.action()
    curr_instruction: bitarray = bus.DataBus.read().copy()

    # Guardar instrucción en la ALU
    ALU.write_register(ALU.IR, curr_instruction)

    # Incrementar PC
    pc_content: int = NC.bitarray2natural(curr_pc_word_dir)
    if pc_content == constants.CODE_RANGE[1]:
        pc_content = 0
    else:
        pc_content += 1

    # Guardar PC incrementado
    ALU.write_register(
        ALU.PC, NC.natural2bitarray(
            pc_content, constants.WORDS_SIZE_BITS
        )
    )
    return 0


def decode():
    """
    Decodifica la instrucción almacenada en el registro IR.
    Utiliza la Unidad de Control (CU) para identificar el tipo de instrucción y su opcode.
    """
    IR_word_bin: bitarray = ALU.read_register(ALU.IR).copy()
    CU.decode(IR_word_bin)


def execute():
    try:
        operations[CU.opcode_length][CU.opcode_offset]()
    except KeyError:
        raise ValueError(f"Instrucción {CU.instruction_asm} no definida.")


# -----------------------
# Classes
# -----------------------

class ALU:
    """ Unidad Aritmético Lógica (ALU) del procesador.
    Contiene los registros del procesador y metodos para manipularlos."""

    # Índice de los registros especiales
    PC: int = 0
    SP: int = 1
    IR: int = 2
    STATE: int = 3

    # Índice de los flags dentro del registro ESTADO
    C: int = 0
    P: int = 1
    N: int = 2
    D: int = 3
    registers: np.ndarray[bitarray] = None

    @staticmethod
    def set_up():
        """ 
        Inicializa los registros de la ALU en 0, hay 32 registros donde los primeros 4 son reservados para el PC, SP, IR y ESTADO (0-3). De ahí en adelante, son registros generales (4-31).
        Cada registro es un objeto bitarray de 64 bits.

        En pocas palabras, inicializa una matriz bidimensional de 32 registros, cada uno con un bitarray de 64 bits.
        """
        # 32 registros donde cada uno es un objeto
        ALU.registers = np.empty(32, dtype=object)
        for i in range(32):
            # Cada objeto apunta a un bitarray de 64 bits
            ALU.registers[i] = bitarray(
                '0' * constants.WORDS_SIZE_BITS, endian='big')

    @staticmethod
    def is_register_special(register_id: int):
        """
        Verifica si el registro es uno de los registros especiales (PC, SP, IR, ESTADO).
        Los registros especiales son los primeros 4 registros (0-3).
        :param register_id: ID del registro a verificar.
        :return: True si es un registro especial, False en caso contrario."""
        if 0 <= register_id < 4:
            return True
        return False

    @staticmethod
    def read_register(register_id: int) -> bitarray:
        """
        Lee el registro especificado por register_id y devuelve su contenido como un bitarray de 64 bits.
        """

        content: bitarray = ALU.registers[register_id]

        return content

    @staticmethod
    def write_register(register_id: int, value: bitarray) -> None:
        """
        Escribe el valor en el registro especificado por register_id.
        El valor debe ser un bitarray de 64 bits.
        Si el registro es especial, se lanza una excepción.
        """

        # Obtener la pila de llamadas
        stack = inspect.stack()
        # Nombre de la función llamadora
        caller_name = stack[1].function

        if ALU.is_register_special(register_id):
            if not (
                    caller_name == "preparate" or caller_name == "fetch"
                    or caller_name == "modify_state_int"):
                raise ValueError(
                    f"Registro {register_id} es especial y no se puede escribir directamente.")

        if len(value) != constants.WORDS_SIZE_BITS:
            raise ValueError(
                f"El valor debe tener {constants.WORDS_SIZE_BITS} bits.")

        ALU.registers[register_id] = value.copy()

    @staticmethod
    def modify_state_int(value: int) -> None:
        state: bitarray = NC.natural2bitarray(0, 64)

        valid_length = True
        try:
            _ = NC.int2bitarray(value, constants.WORDS_SIZE_BITS)
        except ValueError:
            valid_length = False

        if value == 0:
            state[constants.WORDS_SIZE_BITS - ALU.C - 1] = 1
        if value > 0:
            state[constants.WORDS_SIZE_BITS - ALU.P - 1] = 1
        if value < 0:
            state[constants.WORDS_SIZE_BITS - ALU.N - 1] = 1
        if not valid_length:
            state[constants.WORDS_SIZE_BITS - ALU.D - 1] = 1

        ALU.write_register(ALU.STATE, state)


class CU:
    """
    Unidad de Control (CU) del procesador.
    Contiene la lógica para decodificar instrucciones y determinar su tipo.
    """
    # Convenciones de segmentos de instrucción
    instruction_word: bitarray = None
    opcode_length: str = None
    opcode_offset: int = None
    instruction_asm: str = None
    instruction_args: list[bitarray] = None

    @staticmethod
    def decode(word_binary: bitarray) -> None:
        """
        Decodifica la instrucción binaria y determina su tipo y opcode.
        :param word_binary: Instrucción binaria de 64 bits.
        :raises ValueError: Si la instrucción no es de 64 bits o no se encuentra el opcode.
        """
        if len(word_binary) != constants.WORDS_SIZE_BITS:
            raise ValueError(f"Instruction must be of 64 bits")

        CU.instruction_word = word_binary

        # Encontrar de qué tipo es la instrucción y cuál es su opcode.
        opcodes_dict = utils.FileManager.JSON.JSON2dict(constants.OPCODES_PATH)
        length, offset = None, None
        instr_str = str(CU.instruction_word.to01())  # Convertir a string la cadena de bits

        for length_i, opcodes_list in opcodes_dict.items():
            for idx, opcode in enumerate(opcodes_list):
                if instr_str.startswith(opcode):
                    length = length_i
                    offset = idx
                    break
            if length is not None:
                break  # Salir del ciclo exterior si ya se encontró

        if length is None:
            raise ValueError(
                "No existe opcode con el que inicie la instrucción.")

        CU.opcode_length = length
        CU.opcode_offset = offset

        # Obtener la instrucción exacta
        instr_asm_dict: dict = utils.FileManager.JSON.JSON2dict(constants.ISA_PATH)
        CU.instruction_asm = instr_asm_dict[CU.opcode_length][CU.opcode_offset]

        # Extract args depending on length type
        CU.instruction_args = []
        if length == "64":
            CU.instruction_args.append(CU.instruction_word)  # Code instruction
        elif length == "54":
            CU.instruction_args.append(CU.instruction_word[0:54])  # Opcode
            CU.instruction_args.append(CU.instruction_word[54:59])  # R
            CU.instruction_args.append(CU.instruction_word[59:64])  # R'
        elif length == "59":
            CU.instruction_args.append(CU.instruction_word[0:59])  # Opcode
            CU.instruction_args.append(CU.instruction_word[59:64])  # R
        elif length == "35":
            CU.instruction_args.append(CU.instruction_word[0:35])  # Opcode
            CU.instruction_args.append(CU.instruction_word[35:40])  # R
            CU.instruction_args.append(CU.instruction_word[40:64])  # M
        elif length == "27":
            CU.instruction_args.append(CU.instruction_word[0:27])  # Opcode
            CU.instruction_args.append(CU.instruction_word[27:32])  # R
            CU.instruction_args.append(CU.instruction_word[32:64])  # V
        elif length == "40":
            CU.instruction_args.append(CU.instruction_word[0:40])  # Opcode
            CU.instruction_args.append(CU.instruction_word[40:64])  # M


class ISA:
    # TODO: Refactorizar la ISA para que use bitarray y no listas de enteros, además use los metodos de después de la refactorización.
    # ------------------
    # Type Code
    # ------------------
    class C:

        @staticmethod
        def para():
            global PARA_INSTRUCTION
            PARA_INSTRUCTION = True

    # ------------------
    # Type R
    # ------------------

    class R:
        @staticmethod
        def suma():
            """ Suma de Enteros. """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(ALU.read_register(r_p))

            value: int = v1 + v2
            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

        @staticmethod
        def resta():
            """ Resta de Enteros. """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(ALU.read_register(r_p))

            value: int = v1 - v2
            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

        @staticmethod
        def mult():
            """ Multiplicación de Enteros. """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(ALU.read_register(r_p))

            value: int = v1 * v2
            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

        @staticmethod
        def divi():
            """ División de Enteros. """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(ALU.read_register(r_p))

            value: int = v1 // v2
            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

        @staticmethod
        def y_bit_bit():
            """ Bitwise and """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: bitarray = ALU.read_register(r)
            v2: bitarray = ALU.read_register(r_p)

            value: bitarray = v1 & v2
            ALU.write_register(r, value)

        @staticmethod
        def o_bit_bit():
            """ Bitwise Or """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: bitarray = ALU.read_register(r)
            v2: bitarray = ALU.read_register(r_p)

            value: bitarray = v1 | v2
            ALU.write_register(r, value)

        @staticmethod
        def xor_bit_bit():
            """ Bitwise Xor """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: bitarray = ALU.read_register(r)
            v2: bitarray = ALU.read_register(r_p)

            value: bitarray = v1 ^ v2
            ALU.write_register(r, value)

        @staticmethod
        def comp():
            """Comparar Enteros"""
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(ALU.read_register(r_p))

            value_cmp: int = v1 - v2
            ALU.modify_state_int(value_cmp)

        @staticmethod
        def copia():
            """Copiar contenido de registro"""
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            r_p: int = NC.bitarray2natural(CU.instruction_args[2])

            v1: bitarray = ALU.read_register(r_p).copy()

            ALU.write_register(r, v1)

        @staticmethod
        def not_bit_bit():
            """Not Bitwise"""
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            v1: bitarray = ALU.read_register(r).copy()

            v1 = ~v1

            ALU.write_register(r, v1)

        @staticmethod
        def limpia():
            """Limpia un registro"""
            r: int = NC.bitarray2natural(CU.instruction_args[1])

            ALU.write_register(r, NC.int2bitarray(0, 64))

        @staticmethod
        def incr():
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            value: int = NC.bitarray2int(ALU.read_register(r)) + 1

            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

        @staticmethod
        def decr():
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            value: int = NC.bitarray2int(ALU.read_register(r)) - 1

            ALU.modify_state_int(value)
            ALU.write_register(r, NC.int2bitarray(value, 64, truncate=True))

    # ------------------
    # Type I
    # ------------------

    class I_:

        @staticmethod
        def cargar():
            """
            Contenido dirección de memoria a registro
            """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            m_bin: bitarray = CU.instruction_args[2]

            bus.DirectionBus.write(m_bin)
            bus.ControlBus.write(bus.ControlBus.READ_MEMORY_BIN)
            bus.action()
            word: bitarray = bus.DataBus.read().copy()

            ALU.write_register(r, word)

        @staticmethod
        def guardar():
            """
            Contenido de un registro en una dirección de memoria
            """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            m_bin: bitarray = CU.instruction_args[2]

            word: bitarray = ALU.read_register(r).copy()

            bus.DirectionBus.write(m_bin)
            bus.ControlBus.write(bus.ControlBus.WRITE_MEMORY_BIN)
            bus.DataBus.write(word)
            bus.action()

        @staticmethod
        def carga_inm():
            """
            Cargar un entero inmediato (32 bits) al registro en
                los bits menos significativos.
                Lo convierte a 64 bits para dejarlo como nuevo.
            """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            v: bitarray = CU.instruction_args[2]

            v = NC.extend_bitarray(v, constants.WORDS_SIZE_BITS)

            ALU.write_register(r, v)

        @staticmethod
        def carga_inm_superior():
            """
            #Cargar un entero inmediato (32 bits) al registro en
            #los bits más significativos
            """
            r: int = NC.bitarray2natural(CU.instruction_args[1])

            # Value most significant bits
            v_m: bitarray = CU.instruction_args[2]
            # Value less significant bits
            v_l: bitarray = NC.truncate_bitarray_ls(ALU.read_register(r).copy(), 32)

            long_bin: bitarray = v_m + v_l

            ALU.write_register(r, long_bin)

        @staticmethod
        def suma_inm():
            """
            Suma enteros el registro destino con un entero inmediato
            """
            r: int = NC.bitarray2natural(CU.instruction_args[1])
            v1: int = NC.bitarray2int(ALU.read_register(r))
            v2: int = NC.bitarray2int(CU.instruction_args[2])

            value_result: int = v1 + v2
            ALU.write_register(
                r, NC.int2bitarray(
                    value_result, constants.WORDS_SIZE_BITS,
                    truncate=True
                )
            )

            ALU.modify_state_int(value_result)


# ------------------------------------
# ------------------------------------

operations: dict[str, list[Callable[[], None]]] = {
    "64": [
        "PROCRASTINA", "VUELVE", ISA.C.para
    ],
    "54": [
        ISA.R.suma, ISA.R.resta, ISA.R.mult, ISA.R.divi, ISA.R.y_bit_bit,
        ISA.R.o_bit_bit, ISA.R.xor_bit_bit, ISA.R.comp, ISA.R.copia
    ],
    "59": [
        ISA.R.not_bit_bit, ISA.R.limpia, ISA.R.incr, ISA.R.decr, "APILA", "DESAPILA"
    ],
    "35": [
        ISA.I_.cargar, ISA.I_.guardar, "SIREGCERO", "SIREGNCERO"
    ],
    "27": [
        ISA.I_.carga_inm, ISA.I_.carga_inm_superior, ISA.I_.suma_inm, "IRESTA", "IMULT",
        "IDIVI", "IAND", "IOR", "IXOR", "ICOMP"
    ],
    "40": [
        "SALTA", "LLAMA", "SICERO", "SINCERO", "SIPOS", "SINEG",
        "SIOVERFL", "SIMAYOR", "SIMENOR", "INTERRUP"
    ]
}
