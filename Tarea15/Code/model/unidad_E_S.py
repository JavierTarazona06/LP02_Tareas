import utils
import constants

from model import memory

codigo_modulo = "ES"

def leer_dispositivo(direccion: int):
    if utils.check_addres_operation(codigo_modulo, direccion):
        memory.leer(direccion)
    else:
        raise Exception("La dirección para E/S no esta en el rango válido")

def escribir_dispositivo(direccion: int, palabra_decimal: int):
    if utils.check_addres_operation(codigo_modulo, direccion):
        memory.escribir(direccion, palabra_decimal)
    else:
        raise Exception("La dirección para E/S no esta en el rango válido")


