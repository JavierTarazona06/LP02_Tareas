import struct
from typing import Optional

import constants


class NumberConversion:

    @staticmethod
    def binary_list2entero(binary_list: list[int]) -> int:
        """
        Convierte una lista de bits (0 y 1) en su valor decimal
        usando complemento a dos.
        """
        if not binary_list:
            raise ValueError("La lista de bits no puede estar vacía.")

        if not all(isinstance(b, int) and b in (0, 1) for b in binary_list):
            raise ValueError("Todos los elementos deben ser enteros 0 o 1.")

        bit_string = ''.join(str(b) for b in binary_list)
        n_bits = len(binary_list)

        # Análisis del complemento a 2
        if binary_list[0] == 1:
            # Complemento a 2
            return int(bit_string, 2) - (1 << n_bits) # 2^n_bits para obtener negativo
        else:
            return int(bit_string, 2)

    @staticmethod
    def entero2binary_list(
            n: int, fix_bits: Optional[int] = constants.WORDS_SIZE_BITS
    ) -> list[int]:
        """
        Convierte un número decimal (positivo o negativo) a una
        lista de bits en complemento a dos.
        """
        if not isinstance(n, int):
            raise ValueError("El número debe ser un entero.")

        # Si se especifican bits fijos, verificar si el número cabe en complemento a 2
        if fix_bits is not None:
            if not isinstance(fix_bits, int) or fix_bits <= 0:
                raise ValueError("fix_bits debe ser un entero positivo.")
            # Toma el menor valor decimal con 2^(fix_bits - 1) bits
            min_val = - (1 << (fix_bits - 1))
            # Toma el mayor valor decimal con 2^(fix_bits - 1) bits -1 por el cero
            max_val = (1 << (fix_bits - 1)) - 1
            if not (min_val <= n <= max_val):
                raise ValueError(f"El número {n} no se puede representar "
                                 f"con {fix_bits} bits en complemento a 2.")
            bits = fix_bits
        else:
            # Calcular bits mínimos necesarios para representar el número en complemento a 2
            if n >= 0:
                bits = n.bit_length() + 1  # +1 para el bit de signo
            else:
                bits = (-n).bit_length() + 1

        if n >= 0:
            bin_str = bin(n)[2:].zfill(bits)
        else:
            bin_str = bin((1 << bits) + n)[2:]  # complemento a dos de `n` negativo

        return [int(bit) for bit in bin_str.zfill(bits)]

    @staticmethod
    def binary_list2natural(binary_list: list[int]) -> int:
        """
        Sin complemento a 2
        """
        binary_list = [0] + binary_list
        return NumberConversion.binary_list2entero(binary_list)

    @staticmethod
    def natural2binary_list(
            n: int, fix_bits: Optional[int] = constants.WORDS_SIZE_BITS
    ) -> list[int]:
        """
        Sin complemento a 2
        """
        if fix_bits:
            bin_list:list[int] = NumberConversion.entero2binary_list(n, fix_bits + 1)
        else:
            bin_list:list[int] = NumberConversion.entero2binary_list(n, None)
        # Le quito el signo
        bin_list = bin_list[1:]
        return bin_list

    @staticmethod
    def double2binary_list(value: float) -> list[int]:
        """
        Convierte un número de punto flotante (IEEE 754 doble precisión)
        a una lista de 64 bits (enteros 0 o 1).
        """
        if not isinstance(value, float):
            raise ValueError("El valor debe ser un "
                             "número de punto flotante (float).")

        # Empaquetar en formato IEEE 754 de doble precisión y convertir a bits
        packed = struct.pack('>d', value)  # big-endian double, byte mas significativo primero
        bits = ''.join(f'{byte:08b}' for byte in packed)
        return [int(b) for b in bits]

    @staticmethod
    def binary_list2double(binary_list: list[int]) -> float:
        """
        Convierte una lista de 64 bits (enteros 0 o 1) en un número flotante
        usando el estándar IEEE 754 de doble precisión.
        """
        if len(binary_list) != 64:
            raise ValueError("La lista debe contener exactamente 64 bits.")

        if not all(b in (0, 1) for b in binary_list):
            raise ValueError("Todos los elementos deben ser 0 o 1.")

        bit_string = ''.join(str(b) for b in binary_list)
        byte_data = int(bit_string, 2).to_bytes(8, byteorder='big')
        return struct.unpack('>d', byte_data)[0]


def check_address_operation(operator: str, direccion: int) -> bool:
    operators = {
        "C": constants.CODE_RANGE,
        "ES": constants.E_S_RANGE,
        "D": constants.DATA_RANGE,
        "S": constants.STACK_RANGE,
    }
    if operator in operators:
        range = operators[operator]
    else:
        raise ValueError("Operador invalido")

    return range[0] <= direccion <= range[1]
