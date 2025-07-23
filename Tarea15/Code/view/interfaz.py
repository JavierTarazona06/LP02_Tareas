import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

from controller.computer import Action, Data


class SimuladorComputador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Computador")
        self.geometry("1000x600")
        self._crear_scroll_general()

        # Inicializar el backend
        Action.start_emulation()

    def _crear_scroll_general(self):
        contenedor = tk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(contenedor, bg='gray90')
        scrollbar = ttk.Scrollbar(
            contenedor, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg='gray80')

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._crear_area_codigo()
        self._crear_area_ejecucion()

    def _crear_area_codigo(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Código Ensamblador o Binario", padding=10)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text="Código:").pack(anchor="w")
        self.codigo_text = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.codigo_text.pack()

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)

        self.btn_cargar_archivo = ttk.Button(
            btn_frame, text="Cargar desde Archivo", command=self._cargar_archivo)
        self.btn_cargar_archivo.pack(side="left", padx=5)

        ttk.Label(btn_frame, text="Dirección de carga (hex):").pack(side="left")
        self.direccion_carga = ttk.Entry(btn_frame, width=10)
        self.direccion_carga.pack(side="left", padx=5)

        self.btn_enlazar = ttk.Button(
            btn_frame, text="Cargar a Memoria", command=self._enlazar_codigo)
        self.btn_enlazar.pack(side="left", padx=5)

    def _cargar_archivo(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de código",
               filetypes=(("Archivos de texto", "*.txt"),("Archivos de configuración", "*.in"),("Todos los archivos", "*.*")
    )
        )
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                contenido = file.read()
                self.codigo_text.delete(1.0, tk.END)
                self.codigo_text.insert(tk.END, contenido)

    def _enlazar_codigo(self):
        codigo = self.codigo_text.get(1.0, tk.END).strip()
        direccion = self.direccion_carga.get()
        if codigo and direccion:
            try:
                direccion_int = int(direccion, 16)
                Action.load_machine_code(codigo, direccion_int)
                tk.messagebox.showinfo("Éxito", "Código cargado correctamente en la memoria.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo cargar: {e}")
        else:
            tk.messagebox.showwarning("Atención", "Falta código o dirección.")

    def _crear_area_ejecucion(self):
        frame = ttk.LabelFrame(self.scroll_frame, text="Ejecutar Programa", padding=10)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text="Dirección de inicio (hex):").pack(anchor="w")
        self.dir_inicio = ttk.Entry(frame, width=15)
        self.dir_inicio.pack(anchor="w", pady=5)

        self.btn_ejecutar = ttk.Button(
            frame, text="Ejecutar Programa", command=self._ejecutar_programa)
        self.btn_ejecutar.pack(pady=5)

        self.output_ejecucion = scrolledtext.ScrolledText(frame, width=100, height=10)
        self.output_ejecucion.pack()

    def _ejecutar_programa(self):
      direccion = self.dir_inicio.get()
      if direccion:
        try:
            direccion_int = int(direccion, 16)
            Action.execute_progam(direccion_int)
            self.output_ejecucion.insert(
                tk.END, f"Programa ejecutado desde dirección {direccion}.\n")

            # ✅ Leer solo la posición de resultado:
            direccion_resultado = 131072
            resultado = Data.Memory_D.get_memory_content(direccion_resultado, "decimal")

            self.output_ejecucion.insert(
                tk.END, f"Resultado guardado en memoria[{direccion_resultado}]: {resultado}\n")

        except Exception as e:
            self.output_ejecucion.insert(tk.END, f"Error: {e}\n")
      else:
          self.output_ejecucion.insert(tk.END, "Dirección de inicio vacía.\n")



if __name__ == "__main__":
    app = SimuladorComputador()
    app.mainloop()
