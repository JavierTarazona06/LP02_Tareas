import numpy as np
from bitarray import bitarray

import constants
from model.procesador.CPU import ALU
from utils import NumberConversion as NC
from model.procesador.memory import Memory
from model.procesador.bus import DataBus, DirectionBus, ControlBus

# -----------------------
# Public Global Variables
# -----------------------

# Código de máquina donde cada línea está separada por un \n
MACHINE_CODE: str = None


# -----------------------
# Funciones de acción
# -----------------------

class Action:

    @staticmethod
    def start_simulation() -> int:
        # Inicializar componentes

        # Desplegar interfaz grafica

        # Retornar
            # 0 exito
            # -1 fracaso
        pass

    @staticmethod
    def stop_simulation() -> None:
        # Cerrar programa
        # Guardar archivos?
        # Llamar CPU Refresh
        pass

    @staticmethod
    def load_machine_code(address: int):
        """
        Load machine code at the given address
        """
        # Convertir machine_code en una lista separada por \n

        # Tomar de a línea i=0 por línea de machine_code
            # 64 por 64 digitos binarios
            # Tener en cuenta que cada 0, 1 es +1 en conteo
            # pero cuando haya un {n},y se reemplaza por (address + n)
            # en binario y se suma su longitud al conteo.
            # El conteo es una verificación de apoyo, si una línea no tiene

            # Cuando se tenga la palabra de 64 bits pasarla a bitarray, se
            # pone el Bus de dirección en address + i, el de control en
            # write memory y el de datos se pone esa palabra que esta ingresando.
            # Se corre bus.action() para scribir en la memoria.


    @staticmethod
    def execute_instruction(address: int):
        """
        Execute a specific instruction from a given address
        """
        # Pone el contenido del PC de la ALU en la
        # dirección adress como de natural a bitarray

        # Poner CPU.EN_EJECUCION = True

        # Llama a fetch de CPU
        # Llama a decode de CPU
        # Llama a execute de CPU

        # Llama CPU.reset(), pone CPU.en ejecución y CPU.para en False

    @staticmethod
    def execute_progam(address: int):
        """
        Start program execution with the instruction from a given address
        """
        # Pone el contenido del PC de la ALU en la
        # dirección adress como de natural a bitarray

        # Poner CPU.EN_EJECUCION = True

        # Mientras que CPU.PARA sea False:
            # Llama a fetch de CPU
            # Llama a decode de CPU
            # Llama a execute de CPU

        # Llama CPU.reset(), pone CPU.en ejecución y CPU.para en False


# -----------------------
# Funciones de datos
# -----------------------

class Code_Management:
    @staticmethod
    def set_machine_code(machine_code: str):
        """
        Guarda el machine code, como código de máquina relocalizable.
        Las separaciones deben ser con \n
        """
        MACHINE_CODE = machine_code

class Data:

    class Memory_D:

        @staticmethod
        def get_memory_content(address: int, mode: str) -> str:
            """
            Devuelve la palabra almacenada en una dirección de memoria en el formato solicitado.

            :param address: Dirección de memoria.
            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Cadena representando la palabra en el formato especificado.
            """
            valid_modes = ["bin", "hex", "decimal", "decimalc2"]
            if mode not in valid_modes:
                raise ValueError(f"Modo inválido: '{mode}'. Opciones válidas: {valid_modes}")

            word_64: np.uint64 = Memory.read(address)
            word_bit: bitarray = NC.natural2bitarray(int(word_64))

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(int(word_64))
            elif mode == "decimal":
                return str(int(word_64))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))

        @staticmethod
        def get_memory_range_content(start: int, end: int, mode: str) -> list[str]:
            """
            Devuelve el contenido de un rango de direcciones de memoria en el formato especificado.

            :param start: Dirección inicial del rango (inclusive).
            :param end: Dirección final del rango (inclusive).
            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Lista de cadenas con el contenido de cada dirección en el formato solicitado.
            """
            if start > end:
                raise ValueError(
                    "La dirección inicial debe ser menor o "
                    "igual a la dirección final."
                )

            return [Data.Memory_D.get_memory_content(addr, mode) for addr in range(start, end + 1)]

        @staticmethod
        def get_code_segment_content(mode: str) -> list[str]:
            """
            Devuelve el contenido del segmento de código en el formato especificado.
            """
            return Data.Memory_D.get_memory_range_content(
                constants.CODE_RANGE[0], constants.CODE_RANGE[1],
                mode
            )

        @staticmethod
        def get_es_segment_content(mode: str) -> list[str]:
            """
            Devuelve el contenido del segmento de entrada/salida en el formato especificado.
            """
            return Data.Memory_D.get_memory_range_content(
                constants.E_S_RANGE[0], constants.E_S_RANGE[1],
                mode
            )

        @staticmethod
        def get_data_segment_content(mode: str) -> list[str]:
            """
            Devuelve el contenido del segmento de datos en el formato especificado.
            """
            return Data.Memory_D.get_memory_range_content(
                constants.DATA_RANGE[0], constants.DATA_RANGE[1],
                mode
            )

        @staticmethod
        def get_stack_segment_content(mode: str) -> list[str]:
            """
            Devuelve el contenido del segmento de pila (stack) en el formato especificado.
            """
            return Data.Memory_D.get_memory_range_content(
                constants.STACK_RANGE[0], constants.STACK_RANGE[1],
                mode
            )

    class CPU_D:
        @staticmethod
        def get_register_content(reg_num: int, mode: str) -> str:
            """
            Devuelve la palabra almacenada en una dirección de registros en el formato solicitado.

            PC, SP, IR, ESTADO, R4, ..., R31

            0,  1,   2,    3,   4,  ..., 31

            :param reg_num: Numero del registro
            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Cadena representando la palabra en el formato especificado.
            """
            valid_modes = ["bin", "hex", "decimal", "decimalc2"]
            if mode not in valid_modes:
                raise ValueError(f"Modo inválido: '{mode}'. Opciones válidas: {valid_modes}")

            word_bit: bitarray = ALU.read_register(reg_num)

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(NC.bitarray2natural(word_bit))
            elif mode == "decimal":
                return str(NC.bitarray2natural(word_bit))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))

    class Bus_D:

        @staticmethod
        def get_databus(mode: str) -> str:
            """
            Devuelve el contenido del bus de datos en el formato solicitado.

            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Cadena representando la palabra en el formato especificado.
            """
            valid_modes = ["bin", "hex", "decimal", "decimalc2"]
            if mode not in valid_modes:
                raise ValueError(f"Modo inválido: '{mode}'. Opciones válidas: {valid_modes}")

            word_bit: bitarray = DataBus.read()

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(NC.bitarray2natural(word_bit))
            elif mode == "decimal":
                return str(NC.bitarray2natural(word_bit))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))


        @staticmethod
        def get_directionbus(mode: str) -> str:
            """
            Devuelve el contenido del bus de dirección en el formato solicitado.

            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Cadena representando la palabra en el formato especificado.
            """
            valid_modes = ["bin", "hex", "decimal", "decimalc2"]
            if mode not in valid_modes:
                raise ValueError(f"Modo inválido: '{mode}'. Opciones válidas: {valid_modes}")

            word_bit: bitarray = DirectionBus.read()

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(NC.bitarray2natural(word_bit))
            elif mode == "decimal":
                return str(NC.bitarray2natural(word_bit))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))

        @staticmethod
        def get_controlbus(mode: str) -> str:
            """
            Devuelve el contenido del bus de dirección en el formato solicitado.

            :param mode: Modo de representación ('bin', 'hex', 'decimal', 'decimalc2').
            :return: Cadena representando la palabra en el formato especificado.
            """
            valid_modes = ["bin", "hex", "decimal", "decimalc2"]
            if mode not in valid_modes:
                raise ValueError(f"Modo inválido: '{mode}'. Opciones válidas: {valid_modes}")

            word_bit: bitarray = ControlBus.read()

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(NC.bitarray2natural(word_bit))
            elif mode == "decimal":
                return str(NC.bitarray2natural(word_bit))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))