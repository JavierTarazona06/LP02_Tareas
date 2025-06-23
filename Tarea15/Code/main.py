from utils import FileManager
from controller import computer
print("!")

if __name__ == '__main__':
    computer.Action.start_emulation()
    machine_code_str:str = FileManager.TXT.read_file_as_str(r"Ejemplos/suma.in")
    computer.Action.load_machine_code(machine_code_str, 5)
    computer.Action.execute_progam(5)
    computer.Action.stop_emulation(True, True, "bin")