import numpy as np
from bitarray import bitarray

import constants
from utils import NumberConversion as NC
from model.procesador import bus

class Enlazador:
    # Código de máquina donde cada línea está separada por un \n
    MACHINE_CODE_RELOC: list[str] = None

    @staticmethod
    def set_machine_code(machine_code_reloc: str):
        """
        Guarda el machine code, como código de máquina relocalizable.
        Las instrucciones deben estar separadas por saltos de línea (\n).

        :param machine_code_reloc: Cadena con instrucciones en código máquina separadas por \n.
        """

        if not isinstance(machine_code_reloc, str):
            raise TypeError("El código de máquina debe ser una cadena (str).")

        machine_code_reloc_lines: list[str] = machine_code_reloc.strip().split('\n')
        if (len(machine_code_reloc_lines) < 1 or
                any(not line.strip()
                    for line in machine_code_reloc_lines)):
            raise ValueError(
                "La cadena debe contener líneas "
                "separadas por '\\n', sin líneas vacías."
            )

        Enlazador.MACHINE_CODE_RELOC = machine_code_reloc_lines

    @staticmethod
    def link_load_machine_code(address: int):
        """
        Carga el código de máquina relocalizable
        en la posición:
        :param address: número natural de 0 a 65535
        """
        if not (0 <= address <= constants.CODE_RANGE[1]):
            raise ValueError(
                f"Dirección {address} inválida para "
                f"el área del código"
            )

        for idx, code_line in enumerate(Enlazador.MACHINE_CODE_RELOC):
            bits_count = 0
            # Contar 0 y 1
            bits_count += code_line.count('0') + code_line.count('1')

            # Reemplazar {natural} si existe
            if '{' in code_line and '}' in code_line:
                start = code_line.find('{') + 1
                end = code_line.find('}')
                natural_str = code_line[start:end]

                try:
                    natural_val = int(natural_str)
                except ValueError:
                    raise ValueError(f"Línea {idx}: "
                                     f"valor no "
                                     f"numérico en {{...}}: '{natural_str}'")

                direccion_relocalizada = natural_val + address
                # 24 bits con ceros a la izquierda
                direccion_bin: str = (
                    format(direccion_relocalizada, '024b'))

                # Reemplazar la subcadena completa "{...}" por el binario
                code_line:str = code_line.replace(
                    f'{{{natural_str}}}', direccion_bin)

                # Contar bits del nuevo binario insertado
                bits_count += len(direccion_bin)

                if bits_count != constants.WORDS_SIZE_BITS:
                    raise ValueError(f"Instrucción {idx} no tiene 64 bits")

                instruction_bin: bitarray = bitarray(code_line)

                bus.DirectionBus.write(NC.natural2bitarray(address+idx, 24))
                bus.ControlBus.write(bus.ControlBus.WRITE_MEMORY)
                bus.DataBus.write(instruction_bin)
                bus.action()


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