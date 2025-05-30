import numpy as np
from bitarray import bitarray

import constants
from utils import NumberConversion as NC
from utils import FileManager

from model.procesador import CPU
from model.procesador import unidad_E_S
from model.procesador.memory import Memory
from model.enlazador.enlazador import Enlazador

from model.procesador import bus
from model.procesador.bus import DataBus, DirectionBus, ControlBus


# -----------------------
# Public Global Variables
# -----------------------

# -----------------------
# Funciones de acción
# -----------------------

class Action:

    @staticmethod
    def start_emulation() -> int:
        """
        Inicializar componentes y desplegar interfaz gráfica.
        Se llama desde el main para ejecutar tod0.

        return:
            0 éxito
            -1 fracaso
        """

        # Inicializar componentes
        bus.set_up()
        CPU.refresh()
        CPU.ALU.set_up()
        Memory.set_up()

        # Desplegar interfaz grafica
        # TODO @sebastian desplegar

        # Retornar
        return 0
        # -1 fracaso
        pass

    @staticmethod
    def stop_emulation(
            save_memory: bool = False, save_registers: bool = False,
            mode: str = "bin"
    ) -> None:
        """
        Función que detiene toda la emulación.

        La idea es que un botón del front "Apagar",
        llama a esta función para que guarde tod0.

        Si en el front se seleccionó, "Guardar Memoria" o "Guardar Registros",
        entonces los parámetros deben ser True respectivamente.
        """
        valid_modes = ["bin", "hex", "decimal", "decimalc2"]
        if mode not in valid_modes:
            raise ValueError(
                f"Modo inválido: '{mode}'. "
                f"Opciones válidas: {valid_modes}")

        # Guardar memoria si requerido en .csv
        if save_memory:
            cells_data: list[str] = (
                Data.Memory_D.
                get_memory_range_content(
                    0, constants.STACK_RANGE[1], mode
                )
            )
            FileManager.CSV.list_to_csv(cells_data, constants.MEMORY_SAVE_PATH)

        # Guardar memoria si requerido en .csv
        if save_registers:
            registers_data: list[str] = (
                Data.CPU_D.get_registers_range_content(
                    0, constants.REGISTERS_SIZE - 1, mode
                )
            )
            FileManager.CSV.list_to_csv(registers_data, constants.REGISTERS_SAVE_PATH)

        # Cerrar interfaz gráfica
        # TODO @sebastian

        # Refrescar la CPU
        CPU.refresh()

        return

    @staticmethod
    def load_machine_code(machine_code_reloc: str, address: int):
        """
        Load machine code at the given address.

        El usuario puede escribir el código de máquina relocalizable en
        una ventana de exto fija en la APp.
        En la parte inferior debe haber un botón que diga enlazar
        y a la izquierda, un campo de texto donde se pueda poner la
        dirección, que es el área del código.

        Al darle click al botón,se llama a esta función con:
        :param machine_code_reloc un string, el código de máquina
            relocalizable que
            contiene '\n'para separar cada línea
        :param address número de 0 a 65535
        """
        # Verificar machine_code en una lista separada por '\n'
        Enlazador.set_machine_code(machine_code_reloc)

        # Cargar código
        Enlazador.link_load_machine_code(address)

    @staticmethod
    def execute_instruction(address: int):
        """
        Execute a specific instruction from a given address

        En el front debe haber un botón "Ejecutar Instrucción"
        Y una caja de texto donde se escribe la
        primera instrucción que se desea ejecutar.

        Al oprimir el botón, el PC se pone en dicha instrucción
        y se ejecuta solo una.
        """
        # Pone el contenido del PC de la ALU en la
        #   dirección address como bitarray
        CPU.preparate(address)

        # Poner CPU en ejecución
        CPU.EN_EJECUCION = True

        # Ciclo Fetch-Decode-Execute
        CPU.fetch()
        CPU.decode()
        CPU.execute()

        # Refrescar la CPU:
        #   Ejecución e instrucción de parada en Falso
        CPU.refresh()

    @staticmethod
    def execute_progam(address: int):
        """
        Start program execution with the instruction from a given address
        """
        # Pone el contenido del PC de la ALU en la
        #   dirección address como bitarray
        CPU.preparate(address)

        # Poner CPU en ejecución
        CPU.EN_EJECUCION = True

        # Ciclo Fetch-Decode-Execute
        while not CPU.PARA_INSTRUCTION:
            CPU.fetch()
            CPU.decode()
            CPU.execute()

        # Refrescar la CPU:
        #   Ejecución e instrucción de parada en Falso
        CPU.refresh()


# -----------------------
# Funciones de datos
# -----------------------

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
            if start < 0:
                raise ValueError(f"Del rango {start} inválido. Debe ser mayor o igual a 0")
            if end > constants.STACK_RANGE[1]:
                raise ValueError(
                    f"Del rango {end} inválido. "
                    f"Debe ser menor o igual a {constants.STACK_RANGE[1]}")

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

            word_bit: bitarray = CPU.ALU.read_register(reg_num)

            if mode == "bin":
                return word_bit.to01()
            elif mode == "hex":
                return hex(NC.bitarray2natural(word_bit))
            elif mode == "decimal":
                return str(NC.bitarray2natural(word_bit))
            elif mode == "decimalc2":
                return str(NC.bitarray2int(word_bit))

        @staticmethod
        def get_registers_range_content(start: int, end: int, mode: str) -> list[str]:
            """
            Devuelve el contenido de un rango de registros en el formato especificado.

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
            if start < 0:
                raise ValueError(f"Del rango {start} inválido. Debe ser mayor o igual a 0")
            if end > 31:
                raise ValueError(f"Del rango {end} inválido. Debe ser menor o igual a 31")

            return [Data.CPU_D.get_register_content(num, mode) for num in range(start, end + 1)]

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
