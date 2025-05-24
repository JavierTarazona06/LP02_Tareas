import utils

from model.procesador import memory

codigo_modulo = "ES"


def leer_dispositivo(direccion: int):
    if utils.check_address_operation(codigo_modulo, direccion):
        palabra_decimal: int = memory.leer(direccion, mode="int")
    else:
        raise Exception("La dirección para E/S no esta en el rango válido")


def escribir_dispositivo(direccion: int, palabra_decimal: int):
    if utils.check_address_operation(codigo_modulo, direccion):
        memory.escribir(direccion, palabra_decimal, mode="int")
    else:
        raise Exception("La dirección para E/S no esta en el rango válido")
