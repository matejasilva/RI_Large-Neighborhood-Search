import tkinter as tk
from tkinter import filedialog
import os
from tkinter import messagebox
from enums import DestroyMethod, RepairMethod, LNSMethod
from solver.solver import Solver

class LnsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("CVRP LNS Rešavanje")
        self.filepath_var = tk.StringVar(value="Učitaj CVRP fajl (.vrp)")
        self.file_loaded = False
        self.algorithm_var = tk.StringVar(value=LNSMethod.BASIC.value) 
        self.destroy_vars = {}
        self.repair_vars = {}
        self.iterations_var = tk.IntVar(value=1000)
        self.build_ui()

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title = "Selektuj CVRP fajl",
            filetypes = [("VRP files", "*.vrp")],
            initialdir = "./instances"
        )
        if file_path:
            self.filepath_var.set(os.path.basename(file_path))
            self.full_path = file_path
            self.file_loaded = True

    def on_algorithm_selected(self, *args):
        algorithm = self.algorithm_var.get()
        algorithm = LNSMethod(algorithm)

        for var, cb in self.destroy_vars.values():
            cb.config(state="normal")
            var.set(False)

        for var, cb in self.repair_vars.values():
            cb.config(state="normal")
            var.set(False)


        if algorithm == LNSMethod.BASIC:
            for var, cb in self.destroy_vars.values():
                cb.config(command=lambda v=var: self.basic_destroy_selected(v))

            for var, cb in self.repair_vars.values():
                cb.config(command=lambda v=var: self.basic_repair_selected(v))

        else:
            for var, cb in self.destroy_vars.values():
                cb.config(command=lambda: None)

            for var, cb in self.repair_vars.values():
                cb.config(command=lambda: None)

    def basic_destroy_selected(self, selected_var):
        for var, cb in self.destroy_vars.values():
            if var != selected_var:
                var.set(False)

    def basic_repair_selected(self, selected_var):
        for var, cb in self.repair_vars.values():
            if var != selected_var:
                var.set(False)

    def only_digits(self, new_value):
        return new_value.isdigit() or new_value == "" 
    
    def run_algorithm(self):
        if not self.file_loaded:
            messagebox.showerror("Nije učitan fajl", "Molimo Vas da učitate CVRP fajl pre pokretanja algoritma.")
            return

        algorithm = self.algorithm_var.get()
        algorithm = LNSMethod(algorithm)

        selected_destroy = [name for name, (var, _) in self.destroy_vars.items() if var.get()]
        selected_repair = [name for name, (var, _) in self.repair_vars.items() if var.get()]

        if algorithm == LNSMethod.ADAPTIVE:
            if len(selected_destroy) < 2:
                messagebox.showerror(
                    "Nedovoljno selektovano",
                    "AdaptiveLns zahteva minimalno dve destroy heuristike."
                )
                return
            if len(selected_repair) != 2:
                messagebox.showerror(
                    "Nedovoljno selektovano",
                    "AdaptiveLns zahteva obe repair heuristike."
                )
                return
            
        elif algorithm == LNSMethod.BASIC:
            if len(selected_repair) != 1 or len(selected_destroy) != 1:
                messagebox.showerror(
                    "Nedovoljno selektovano",
                    "BasicLns zahteva tačno jednu destroy i jednu repair heuristiku."
                )
                return
        
        iterations = self.iterations_var.get()
        if iterations <= 0:
            messagebox.showerror("Greška", "Broj iteracija mora biti veći od 0.")
            return
        
        solver = Solver(
            filepath=self.full_path,
            algorithm=algorithm,
            destroy_methods=[DestroyMethod(name) for name in selected_destroy],
            repair_methods=[RepairMethod(name) for name in selected_repair],
            iterations=iterations
        )
        best_solution = solver.solve()

    def build_ui(self):
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.grid(row=0, column=0, sticky="ew")

        self.root.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)

        filepath_entry = tk.Entry(
            top_frame,
            textvariable=self.filepath_var,
            font=("TkDefaultFont", 12),
            state="readonly"
        )

        filepath_entry.grid(row=0, column=0, sticky="ew")

        load_button = tk.Button(
            top_frame,
            text="Učitaj CVRP problem",
            font=("TkDefaultFont", 12),
            command=self.load_file
        )
        load_button.grid(row=1, column=0, sticky="e", pady=(6, 0))


        algorithm_label = tk.Label(
            top_frame,
            text="LNS algoritam:",
            font=("TkDefaultFont", 16)
        )
        algorithm_label.grid(row=2, column=0, sticky="w", pady=(20, 4))

        radio_frame = tk.Frame(top_frame)
        radio_frame.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        radio_frame.grid_columnconfigure(0, weight=1)
        radio_frame.grid_columnconfigure(1, weight=1) 
        
        basic_radio = tk.Radiobutton(
            radio_frame,
            text="BasicLns",
            variable=self.algorithm_var,
            value=LNSMethod.BASIC.value,
            font=("TkDefaultFont", 14)
        )
        basic_radio.grid(row=0, column=0, padx=(0, 20))

        adaptive_radio = tk.Radiobutton(
            radio_frame,
            text="AdaptiveLns",
            variable=self.algorithm_var,
            value=LNSMethod.ADAPTIVE.value,
            font=("TkDefaultFont", 14)
        )
        adaptive_radio.grid(row=0, column=1)

        self.algorithm_var.trace_add("write", self.on_algorithm_selected)


        destroy_label_font = ("TkDefaultFont", 16)
        destroy_font = ("TkDefaultFont", 14)

        destroy_label = tk.Label(
            top_frame,
            text="Destroy heuristika:",
            font=destroy_label_font
        )
        destroy_label.grid(row=4, column=0, sticky="w", pady=(20, 4))

        destroy_frame = tk.Frame(top_frame)
        destroy_frame.grid(row=5, column=0, sticky="ew", pady=(0, 12))
        for i in range(4):
            destroy_frame.grid_columnconfigure(i, weight=1)

        destroy_names = [method.value for method in DestroyMethod]
        for i, name in enumerate(destroy_names):
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(
                destroy_frame,
                text=name,
                variable=var,
                font=destroy_font,
                state="normal"
            )
            cb.grid(row=0, column=i, sticky="ew")
            self.destroy_vars[name] = (var, cb)
            cb.config(command=lambda v=var: self.basic_destroy_selected(v))

        repair_label_font = ("TkDefaultFont", 16)
        repair_font = ("TkDefaultFont", 14)

        repair_label = tk.Label(
            top_frame,
            text="Repair heuristika:",
            font=repair_label_font
        )
        repair_label.grid(row=6, column=0, sticky="w", pady=(20, 4))

        repair_frame = tk.Frame(top_frame)
        repair_frame.grid(row=7, column=0, sticky="ew", pady=(0, 12))

        for i in range(2):
            repair_frame.grid_columnconfigure(i, weight=1)

        repair_names = [method.value for method in RepairMethod]
        for i, name in enumerate(repair_names):
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(
                repair_frame,
                text=name,
                variable=var,
                font=repair_font,
                state="normal"
            )
            cb.grid(row=0, column=i, sticky="ew")
            self.repair_vars[name] = (var, cb)
            cb.config(command=lambda v=var: self.basic_repair_selected(v))

        
        iter_label = tk.Label(
            top_frame,
            text="Broj iteracija:",
            font=("TkDefaultFont", 16)
        )
        iter_label.grid(row=8, column=0, sticky="w", pady=(20, 4))

        iter_entry = tk.Entry(
            top_frame,
            textvariable=self.iterations_var,
            font=("TkDefaultFont", 14),
            validate="key",
            validatecommand=(self.root.register(self.only_digits), '%P'),
            bg="white",
            width=6,
            justify="left"
        )
        iter_entry.grid(row=9, column=0, sticky="w")

        run_button = tk.Button(
            top_frame,
            text="Pokreni",
            command=self.run_algorithm,
            font=("TkDefaultFont", 14),
            width=10,
        )
        run_button.grid(row=10, column=0, sticky="e", pady=(10, 0))

    def run_app(self):
        self.root.mainloop()
