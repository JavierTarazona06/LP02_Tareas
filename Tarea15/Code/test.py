import utils
from utils import NumberConversion as NC
from utils import Math

import unittest

class TestBinaryConversion(unittest.TestCase):

    def test_binary_list2str_basic(self):
        self.assertEqual(NC.binary_list2str([1, 0, 1, 1]), "1011")
        self.assertEqual(NC.binary_list2str([0, 0, 0]), "000")
        self.assertEqual(NC.binary_list2str([]), "")

    def test_str2binary_list_basic(self):
        self.assertEqual(NC.str2binary_list("1011"), [1, 0, 1, 1])
        self.assertEqual(NC.str2binary_list("000"), [0, 0, 0])
        self.assertEqual(NC.str2binary_list(""), [])

    def test_round_trip(self):
        for s in ["0", "1", "10", "11001", "000111000"]:
            binary_list = NC.str2binary_list(s)
            reconstructed = NC.binary_list2str(binary_list)
            self.assertEqual(reconstructed, s)

    def test_str2binary_list_invalid(self):
        with self.assertRaises(ValueError):
            NC.str2binary_list("10201")

        with self.assertRaises(ValueError):
            NC.str2binary_list("abc01")

        with self.assertRaises(ValueError):
            NC.str2binary_list("10 01")  # espacio no permitido

    def test_entero2binary_list_positive(self):
        self.assertEqual(NC.entero2binary_list(5, fix_bits=8), [0,0,0,0,0,1,0,1])
        self.assertEqual(NC.entero2binary_list(0, fix_bits=8), [0]*8)
        self.assertEqual(NC.entero2binary_list(127, fix_bits=8), [0,1,1,1,1,1,1,1])

    def test_entero2binary_list_negative(self):
        self.assertEqual(NC.entero2binary_list(-1, fix_bits=8), [1,1,1,1,1,1,1,1])
        self.assertEqual(NC.entero2binary_list(-128, fix_bits=8), [1,0,0,0,0,0,0,0])
        self.assertEqual(NC.entero2binary_list(-5, fix_bits=8), [1,1,1,1,1,0,1,1])

    def test_binary_list2entero_positive(self):
        self.assertEqual(NC.binary_list2entero([0,0,0,0,0,1,0,1]), 5)
        self.assertEqual(NC.binary_list2entero([0]*8), 0)
        self.assertEqual(NC.binary_list2entero([0,1,1,1,1,1,1,1]), 127)

    def test_binary_list2entero_negative(self):
        self.assertEqual(NC.binary_list2entero([1,1,1,1,1,1,1,1]), -1)
        self.assertEqual(NC.binary_list2entero([1,0,0,0,0,0,0,0]), -128)
        self.assertEqual(NC.binary_list2entero([1,1,1,1,1,0,1,1]), -5)

    def test_round_trip(self):
        for n in range(-128, 128):
            bits = NC.entero2binary_list(n, fix_bits=8)
            recovered = NC.binary_list2entero(bits)
            self.assertEqual(n, recovered, f"Falla en round-trip con n={n}")

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            NC.binary_list2entero([])

        with self.assertRaises(ValueError):
            NC.binary_list2entero([0, 2, 1])

        with self.assertRaises(ValueError):
            NC.entero2binary_list("no es un entero", fix_bits=8)

        with self.assertRaises(ValueError):
            NC.entero2binary_list(200, fix_bits=8)

        with self.assertRaises(ValueError):
            NC.entero2binary_list(5, fix_bits=0)

    def test_natural2binary_list_basic(self):
        self.assertEqual(NC.natural2binary_list(0, fix_bits=8), [0]*8)
        self.assertEqual(NC.natural2binary_list(5, fix_bits=4), [0,1,0,1])
        self.assertEqual(NC.natural2binary_list(15, fix_bits=4), [1,1,1,1])

    def test_binary_list2natural_basic(self):
        self.assertEqual(NC.binary_list2natural([0,0,0,0]), 0)
        self.assertEqual(NC.binary_list2natural([1,0,1]), 5)
        self.assertEqual(NC.binary_list2natural([1,1,1,1]), 15)

    def test_round_trip_fixed_bits(self):
        for n in range(0, 128):
            bits = max(n.bit_length(), 1)
            bin_list = NC.natural2binary_list(n, fix_bits=bits)
            reconstructed = NC.binary_list2natural(bin_list)
            self.assertEqual(n, reconstructed, f"Falla en round-trip con n={n}, bin={bin_list}")

    def test_negative_value_raises(self):
        with self.assertRaises(ValueError):
            NC.natural2binary_list(-1, fix_bits=8)
        with self.assertRaises(ValueError):
            NC.natural2binary_list(-100)

    def test_variable_bits(self):
        # Sin fix_bits
        self.assertEqual(NC.natural2binary_list(5, fix_bits=None), [1,0,1])
        self.assertEqual(NC.natural2binary_list(0, fix_bits=None), [0])



class TestHuffmanSet(unittest.TestCase):
    def test_huffman_set(self):
        # Entrada de prueba
        input_data = [(64, 3), (54, 9), (59, 6), (35, 24), (27, 10), (40, 10)]

        # Generar códigos
        huffman_dict = Math.huffman_set(input_data)

        # Verificar total de códigos generados
        total_expected = sum(q for _, q in input_data)
        total_generated = sum(len(lst) for lst in huffman_dict.values())
        self.assertEqual(total_generated, total_expected, "Cantidad total incorrecta de códigos")

        # Verificar longitudes y estructura
        for length, count in input_data:
            self.assertIn(length, huffman_dict, f"No se encontraron códigos de longitud {length}")
            self.assertEqual(len(huffman_dict[length]), count, f"Cantidad incorrecta de códigos de longitud {length}")

            # Verificar que cada código tenga la longitud correcta
            for code in huffman_dict[length]:
                self.assertEqual(len(code), length, f"Código {code} no tiene longitud {length}")

        # Verificar que el conjunto total sea prefix-free
        all_codes_str = [''.join(map(str, code)) for group in huffman_dict.values() for code in group]
        all_codes_str.sort()
        for i in range(len(all_codes_str) - 1):
            c1 = all_codes_str[i]
            c2 = all_codes_str[i + 1]
            self.assertFalse(c2.startswith(c1), f"Ambigüedad detectada: {c1} es prefijo de {c2}")

if __name__ == '__main__':
    unittest.main()