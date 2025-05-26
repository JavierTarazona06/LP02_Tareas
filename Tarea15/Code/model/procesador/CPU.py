from typing import Callable

import constants
import utils
import numpy as np
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from utils import NumberConversion as NC

from model.procesador import bus

EN_EJECUCION = False


def fetch():
    """
    Lee la siguiente instrucción de memoria y la guarda en el registro IR.
    Incrementa el PC para apuntar a la siguiente instrucción.
    """
    # Leer PC para ver a qué palabra apunta
    curr_pc_word_dir = ALU.registers[ALU.PC]

    # Indicarle al bus de control que lea memoria
    control_instruction = bitarray(
        '0' * constants.WORDS_SIZE_BITS, endian='big')
    control_instruction[0] = bus.ControlBus.READ_MEMORY
    bus.ControlBus.write(control_instruction)

    # Escribir PC en el bus de dirección
    bus.DirectionBus.write(curr_pc_word_dir)

    # Leer la palabra de memoria
    bus.action()
    curr_instruction = bus.DataBus.read()

    # Guardar instrucción en la ALU
    ALU.registers[ALU.IR] = curr_instruction.copy()

    # Incrementar PC
    pc_word_natural = ba2int(curr_pc_word_dir, signed=False)
    if pc_word_natural == constants.CODE_RANGE[1]:
        pc_word_natural = 0
    else:
        pc_word_natural += 1

    # Guardar PC incrementado
    ALU.registers[ALU.PC] = int2ba(
        pc_word_natural, length=constants.WORDS_SIZE_BITS, endian='big')
    return 0


def decode():
    """
    Decodifica la instrucción almacenada en el registro IR.
    Utiliza la Unidad de Control (CU) para identificar el tipo de instrucción y su opcode.
    """
    IR_word_bin: bitarray[constants.WORDS_SIZE_BITS] = ALU.registers[ALU.IR]
    CU.decode(IR_word_bin)


def execute():
    # TODO: Refactorizar según los cambios de bitarray
    try:
        operations[CU.opcode_length][CU.opcode_offset]()
    except KeyError:
        raise ValueError(f"Instrucción {CU.instruction_asm} no definida.")


class ALU:
    """ Unidad Aritmético Lógica (ALU) del procesador.
    Contiene los registros del procesador y metodos para manipularlos."""

    # Indice de los registros especiales
    PC = 0
    SP = 1
    IR = 2
    STATE = 3

    # Indice de los flags dentro del registro ESTADO
    C = 0
    P = 1
    N = 2
    D = 3
    registers: np.ndarray = None

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
    def read_register(register_id: int) -> bitarray[64]:
        """
        Lee el registro especificado por register_id y devuelve su contenido como un bitarray de 64 bits.
        """

        if ALU.is_register_special(register_id):
            raise ValueError(
                f"Registro {register_id} es especial y no se puede leer directamente.")

        return ALU.registers[register_id]

    @staticmethod
    def write_register(register_id: int, value: bitarray[64]) -> None:
        """
        Escribe el valor en el registro especificado por register_id.
        El valor debe ser un bitarray de 64 bits.
        Si el registro es especial, se lanza una excepción.
        """

        if ALU.is_register_special(register_id):
            raise ValueError(
                f"Registro {register_id} es especial y no se puede escribir directamente.")

        if len(value) != constants.WORDS_SIZE_BITS:
            raise ValueError(
                f"El valor debe tener {constants.WORDS_SIZE_BITS} bits.")

        ALU.registers[register_id] = value.copy()

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


# TODO: Implementar la CU con los cambios de todo lo demás
class CU:
    """
    Unidad de Control (CU) del procesador.
    Contiene la lógica para decodificar instrucciones y determinar su tipo.
    """
    # Convenciones de segmentos de instrucción
    instruction_word: bitarray[constants.WORDS_SIZE_BITS] = None
    opcode_length: int = None
    opcode_offset: int = None
    instruction_asm: str = None
    instruction_args: list[bitarray] = None

    @staticmethod
    def decode(word_binary: bitarray[constants.WORDS_SIZE_BITS]) -> None:
        """
        Decodifica la instrucción binaria y determina su tipo y opcode.
        :param word_binary: Instrucción binaria de 64 bits.
        :raises ValueError: Si la instrucción no es de 64 bits o no se encuentra el opcode.
        """
        if len(word_binary) != constants.WORDS_SIZE_BITS:
            raise ValueError(f"Instruction must be of 64 bits")

        CU.instruction_word = word_binary

        # Encontrar de qué tipo es la instrucción y cuál es
        opcodes_dict = utils.FileManager.JSON2dict(constants.OPCODES_PATH)
        length, offset = None, None
        instr_str = NC.binary_list2str(CU.instruction_word)

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
        instr_asm_dict = utils.FileManager.JSON2dict(constants.ISA_PATH)
        CU.instruction_asm = instr_asm_dict[CU.opcode_length][CU.opcode_offset]

        # Extract args depending on length type
        CU.instruction_args = []
        if length == 64:
            CU.instruction_args.append(CU.instruction_word)  # Code instruction
        elif length == 54:
            CU.instruction_args.append(CU.instruction_word[0:54])  # Opcode
            CU.instruction_args.append(CU.instruction_word[54:59])  # R
            CU.instruction_args.append(CU.instruction_word[59:64])  # R'
        elif length == 59:
            CU.instruction_args.append(CU.instruction_word[0:59])  # Opcode
            CU.instruction_args.append(CU.instruction_word[59:64])  # R
        elif length == 35:
            CU.instruction_args.append(CU.instruction_word[0:35])  # Opcode
            CU.instruction_args.append(CU.instruction_word[35:40])  # R
            CU.instruction_args.append(CU.instruction_word[40:64])  # M
        elif length == 27:
            CU.instruction_args.append(CU.instruction_word[0:27])  # Opcode
            CU.instruction_args.append(CU.instruction_word[27:32])  # R
            CU.instruction_args.append(CU.instruction_word[32:64])  # V
        elif length == 40:
            CU.instruction_args.append(CU.instruction_word[0:40])  # Opcode
            CU.instruction_args.append(CU.instruction_word[40:64])  # M


class ISA:
    # TODO: Refactorizar la ISA para que use bitarray y no listas de enteros
    # ------------------
    # Type R
    # ------------------

    class R:
        @staticmethod
        def suma():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") +
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def resta():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") -
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def mult():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") *
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def divi():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") //
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def y_bit_bit():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") &
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def o_bit_bit():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") |
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def xor_bit_bit():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = (
                leer_reg(r, mode="int") ^
                leer_reg(r_p, mode="int")
            )
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def comp():
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
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
            r = NC.binary_list2natural(CU.instruction_args[1])
            r_p = NC.binary_list2natural(CU.instruction_args[2])
            value: int = leer_reg(r_p, mode="int")
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def not_bit_bit():
            r = NC.binary_list2natural(CU.instruction_args[1])
            value: int = ~ leer_reg(r, mode="int")
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def limpia():
            r = NC.binary_list2natural(CU.instruction_args[1])
            ALU.modify_state(0, mode="int")
            escribir_reg(r, 0, mode="int")

        @staticmethod
        def incr():
            r = NC.binary_list2natural(CU.instruction_args[1])
            value: int = leer_reg(r, mode="int") + 1
            ALU.modify_state(value, mode="int")
            escribir_reg(r, value, mode="int")

        @staticmethod
        def decr():
            r = NC.binary_list2natural(CU.instruction_args[1])
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
            r = NC.binary_list2natural(CU.instruction_args[1])
            m = NC.binary_list2natural(CU.instruction_args[2])

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
            r = NC.binary_list2natural(CU.instruction_args[1])
            m = NC.binary_list2natural(CU.instruction_args[2])

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
            r = NC.binary_list2natural(CU.instruction_args[1])
            v: list[int] = CU.instruction_args[2]

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
            r: int = NC.binary_list2natural(CU.instruction_args[1])
            v: list[int] = CU.instruction_args[2]

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
            r: int = NC.binary_list2natural(CU.instruction_args[1])
            v: int = NC.binary_list2natural(CU.instruction_args[2])

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


operations: dict[int, list[Callable[[], None]]] = {
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
