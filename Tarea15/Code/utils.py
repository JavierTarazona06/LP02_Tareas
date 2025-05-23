import constants

class NumberConversion:

    @staticmethod
    def binary_list2decimal(binary_list:list[bool]) -> int:
        # int('1011', 2) → 11
        decimal = int(''.join(map(str, binary_list)), 2)
        return decimal

    @staticmethod
    def decimal2binary_list(n: int, fix_bits=None) -> list[bool]:
        """
        Convierte un número decimal en una lista de bits (bool) de longitud fija.
        """
        if fix_bits:
            if n.bit_length() > fix_bits:
                raise ValueError(f"El número {n} se debe escribir con mas bits"
                                 f"que los indicados: {fix_bits}")
            bits = fix_bits
        else:
            bits = n.bit_length()
        bin_str = bin(n)[2:].zfill(bits)  # '0b...' → quitar prefijo y rellenar ceros a la izquierda
        return [bit == '1' for bit in bin_str]


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