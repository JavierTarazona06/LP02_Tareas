import tkinter as tk
from tkinter import ttk, scrolledtext

class SimuladorComputador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Computador")
        self.geometry("1600x1000")
        self.configure(bg='blue')

        self._crear_scroll_general()

    def _crear_scroll_general(self):
        contenedor = tk.Frame(self, bg='blue')
        contenedor.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(contenedor, bg='blue')
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg='blue')

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._crear_secciones()

    def _crear_secciones(self):
        self._crear_area_codigo()
        self._crear_area_memoria()
        self._crear_area_registros()
        self._crear_area_ejecucion()

    def _crear_area_codigo(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Código", padding=10)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        ttk.Label(frame, text="Código de Alto Nivel").grid(row=0, column=0)
        ttk.Label(frame, text="Código Ensamblador").grid(row=0, column=1)
        ttk.Label(frame, text="Código Máquina Relocalizable").grid(row=0, column=2)

        self.codigo_alto = scrolledtext.ScrolledText(frame, width=28, height=30)
        self.codigo_alto.grid(row=1, column=0, padx=5)

        self.codigo_asm = scrolledtext.ScrolledText(frame, width=28, height=30)
        self.codigo_asm.grid(row=1, column=1, padx=5)

        self.codigo_maquina = scrolledtext.ScrolledText(frame, width=28, height=30)
        self.codigo_maquina.grid(row=1, column=2, padx=5)

    def _crear_area_memoria(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Área de Memoria (16MiB, 4 bloques)", padding=10)
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.areas_memoria = {}

        nombres = ["CODE", "E/S", "DATOS", "PILA"]
        for i, nombre in enumerate(nombres):
            sub_frame = ttk.LabelFrame(frame, text=f"Área {nombre}")
            sub_frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            area = scrolledtext.ScrolledText(sub_frame, width=42, height=12)
            area.pack()
            self.areas_memoria[nombre] = area

    def _crear_area_registros(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Registros (64 bits)", padding=10)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        especiales = ["PC", "SP", "IR", "ESTADO"]
        for i, nombre in enumerate(especiales):
            ttk.Label(frame, text=nombre).grid(row=i, column=0, sticky="w")
            ttk.Entry(frame, width=20).grid(row=i, column=1)

        for i in range(28):
            ttk.Label(frame, text=f"R{i+4}").grid(row=i % 14, column=(i // 14) * 2 + 2, sticky="w")
            ttk.Entry(frame, width=20).grid(row=i % 14, column=(i // 14) * 2 + 3)

    def _crear_area_ejecucion(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Ejecutar Programa", padding=10)
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(frame, text="Dirección de inicio (hex):").grid(row=0, column=0, sticky="w")
        self.dir_inicio = ttk.Entry(frame, width=15)
        self.dir_inicio.grid(row=0, column=1)

        self.btn_ejecutar = ttk.Button(frame, text="Ejecutar", command=self._ejecutar_programa)
        self.btn_ejecutar.grid(row=1, column=0, columnspan=2, pady=10)

        self.output_ejecucion = scrolledtext.ScrolledText(frame, width=85, height=8)
        self.output_ejecucion.grid(row=2, column=0, columnspan=3)

    def _ejecutar_programa(self):
        direccion = self.dir_inicio.get()
        self.output_ejecucion.insert(tk.END, f"Ejecutando programa desde la dirección: {direccion}\n")
        # Aquí iría la llamada al backend
        # backend.ejecutar_desde(int(direccion, 16))

if __name__ == "__main__":
    app = SimuladorComputador()
    app.mainloop()
