# ----------------------------------
# Memory
# ----------------------------------

WORDS_SIZE_BITS = 64
MEMORY_BITS = 24
MEMORY_SIZE = 2**MEMORY_BITS

CODE_RANGE = (0, 65535)
E_S_RANGE = (65536, 131071)
DATA_RANGE = (131072, 2031615)
STACK_RANGE = (2031616, MEMORY_SIZE-1)

# ----------------------------------
# Bus: CONTROL
# ----------------------------------

CONTROL_SIZE = 5

# ----------------------------------
# CPU
# ----------------------------------

REGISTERS_SIZE = 32

INS_TYPE_R = (1, 12)
INS_TYPE_I = (13, 26)
INS_TYPE_J = (27, 40)

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

# ----------------------------------
# Instructions
# ----------------------------------

ISA_PATH = "ISA.json"
OPCODES_PATH = "opcodes.json"
