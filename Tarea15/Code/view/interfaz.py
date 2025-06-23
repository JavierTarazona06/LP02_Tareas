import tkinter as tk
from tkinter import ttk, scrolledtext


class SimuladorComputador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Computador")
        self.geometry("1600x1000")
        self._crear_scroll_general()

    def _crear_scroll_general(self):
        contenedor = tk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(contenedor, bg='gray90')
        scrollbar = ttk.Scrollbar(
            contenedor, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg='gray70')

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

        labels = ["Código de Alto Nivel", "Código Ensamblador",
                  "Código Máquina Relocalizable"]
        self.code_texts = []
        self.line_numbers = []

        for col, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=0, column=col)

            # Line numbers widget
            ln = tk.Text(frame, width=4, height=30, padx=4, takefocus=0,
                         border=0, background='gray90', state='disabled')
            ln.grid(row=1, column=col, sticky="nsw", padx=(0, 0))
            self.line_numbers.append(ln)

            # Editable code widget
            txt = tk.Text(frame, width=28, height=30, wrap="none")
            txt.grid(row=1, column=col, padx=(30, 5))
            self.code_texts.append(txt)

            # Bindings for scrolling and updating line numbers
            txt.bind('<KeyRelease>', self._update_all_line_numbers)
            txt.bind('<MouseWheel>', self._on_mousewheel)
            txt.bind('<Button-4>', self._on_mousewheel)  # Linux scroll up
            txt.bind('<Button-5>', self._on_mousewheel)  # Linux scroll down
            txt.bind('<Configure>', self._update_all_line_numbers)
            txt.bind('<Return>', self._update_all_line_numbers)
            txt.bind('<BackSpace>', self._update_all_line_numbers)
            txt.bind('<<Paste>>', self._update_all_line_numbers)
            txt.bind('<<Cut>>', self._update_all_line_numbers)

            # Synchronize scroll between code and line numbers
            txt['yscrollcommand'] = lambda *args, idx=col: self._sync_scroll(
                idx, *args)

        self._update_all_line_numbers()

    def _update_all_line_numbers(self, event=None):
        for txt, ln in zip(self.code_texts, self.line_numbers):
            ln.config(state='normal')
            ln.delete('1.0', tk.END)
            # Get the number of lines in the code widget
            line_count = int(txt.index('end-1c').split('.')[0])
            # Generate line numbers for each line
            line_numbers_string = "\n".join(str(i)
                                            for i in range(1, line_count + 1))
            ln.insert('1.0', line_numbers_string)
            ln.config(state='disabled')

    def _on_mousewheel(self, event):
        # Determine scroll direction
        if event.num == 5 or event.delta < 0:
            delta = 1
        elif event.num == 4 or event.delta > 0:
            delta = -1
        else:
            delta = 0

        for txt, ln in zip(self.code_texts, self.line_numbers):
            txt.yview_scroll(delta, "units")
            ln.yview_scroll(delta, "units")
        return "break"

    def _sync_scroll(self, idx, *args):
        # Synchronize yview for all code and line number widgets
        for i, (txt, ln) in enumerate(zip(self.code_texts, self.line_numbers)):
            if len(args) == 2 and all(self._is_float(a) for a in args):
                # Called from yscrollcommand, use yview_moveto
                txt.yview_moveto(float(args[0]))
                ln.yview_moveto(float(args[0]))
            else:
                # Called from scroll events, use yview
                txt.yview(*args)
                ln.yview(*args)

    def _is_float(self, value):
        try:
            float(value)
            return True
        except Exception:
            return False

    def _crear_area_memoria(self):
        frame = ttk.LabelFrame(
            self.scroll_frame, text="Área de Memoria (16MiB, 4 bloques)", padding=10)
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.areas_memoria = {}

        nombres = ["CODE", "E/S", "DATOS", "PILA"]
        for i, nombre in enumerate(nombres):
            sub_frame = ttk.LabelFrame(frame, text=f"Área {nombre}")
            sub_frame.grid(row=i//2, column=i % 2, padx=5, pady=5)
            area = scrolledtext.ScrolledText(sub_frame, width=42, height=12)
            area.pack()
            self.areas_memoria[nombre] = area

    def _crear_area_registros(self):
        frame = ttk.LabelFrame(
            self.scroll_frame, text="Registros (64 bits)", padding=10)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        especiales = ["PC", "SP", "IR", "ESTADO"]
        for i, nombre in enumerate(especiales):
            ttk.Label(frame, text=nombre).grid(row=i, column=0, sticky="w")
            ttk.Entry(frame, width=20).grid(row=i, column=1)

        for i in range(28):
            ttk.Label(frame, text=f"R{i+4}").grid(row=i %
                                                  14, column=(i // 14) * 2 + 2, sticky="w")
            ttk.Entry(frame, width=20).grid(row=i %
                                            14, column=(i // 14) * 2 + 3)

    def _crear_area_ejecucion(self):
        frame = ttk.LabelFrame(
            self.scroll_frame, text="Ejecutar Programa", padding=10)
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(frame, text="Dirección de inicio (hex):").grid(
            row=0, column=0, sticky="w")
        self.dir_inicio = ttk.Entry(frame, width=15)
        self.dir_inicio.grid(row=0, column=1)

        self.btn_ejecutar = ttk.Button(
            frame, text="Ejecutar", command=self._ejecutar_programa)
        self.btn_ejecutar.grid(row=1, column=0, columnspan=2, pady=10)

        self.output_ejecucion = scrolledtext.ScrolledText(
            frame, width=85, height=8)
        self.output_ejecucion.grid(row=2, column=0, columnspan=3)

    def _ejecutar_programa(self):
        direccion = self.dir_inicio.get()
        self.output_ejecucion.insert(
            tk.END, f"Ejecutando programa desde la dirección: {direccion}\n")
        # Aquí iría la llamada al backend
        # backend.ejecutar_desde(int(direccion, 16))


if __name__ == "__main__":
    app = SimuladorComputador()
    app.mainloop()
