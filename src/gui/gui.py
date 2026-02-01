import tkinter as tk
from tkinter import filedialog
import os
from tkinter import messagebox

class LnsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("CVRP LNS Solver")
        self.filepath_var = tk.StringVar(value="Load a CVRP instance (.vrp)")
        self.file_loaded = False
        self.algorithm_var = tk.StringVar(value="BasicLns") 
        self.destroy_vars = {}
        self.repair_vars = {}
        self.iterations_var = tk.IntVar(value=1000)
        self.build_ui()

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title = "Select a CVRP Instance File",
            filetypes = [("VRP files", "*.vrp")]
        )
        if file_path:
            self.filepath_var.set(os.path.basename(file_path))
            self.full_path = file_path
            self.file_loaded = True

    def on_algorithm_selected(self, *args):
        algo = self.algorithm_var.get()

        for var, cb in self.destroy_vars.values():
            cb.config(state="normal")
            var.set(False)

        for var, cb in self.repair_vars.values():
            cb.config(state="normal")
            var.set(False)


        if algo == "BasicLns":
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
            messagebox.showerror("No File Loaded", "Please load a CVRP instance file before running the algorithm.")
            return

        algorithm = self.algorithm_var.get()

        selected_destroy = [name for name, (var, _) in self.destroy_vars.items() if var.get()]
        selected_repair = [name for name, (var, _) in self.repair_vars.items() if var.get()]

        if algorithm == "AdaptiveLns":
            if len(selected_destroy) < 2:
                messagebox.showerror(
                    "Invalid Selection",
                    "AdaptiveLns requires at least two destroy heuristics to be selected."
                )
                return
            if len(selected_repair) != 2:
                messagebox.showerror(
                    "Invalid Selection",
                    "AdaptiveLns requires both repair heuristics to be selected."
                )
                return
            
        elif algorithm == "BasicLns":
            if len(selected_repair) != 1 or len(selected_destroy) != 1:
                messagebox.showerror(
                    "Invalid Selection",
                    "BasicLns requires exactly one destroy and one repair heuristic to be selected."
                )
                return
        
        iterations = self.iterations_var.get()
        if iterations <= 0:
            messagebox.showerror("Invalid Input", "Number of iterations must be greater than 0.")
            return
        
        print("All good")

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
            text="Load CVRP Problem",
            font=("TkDefaultFont", 12),
            command=self.load_file
        )
        load_button.grid(row=1, column=0, sticky="e", pady=(6, 0))


        algorithm_label = tk.Label(
            top_frame,
            text="LNS Algorithm:",
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
            value="BasicLns",
            font=("TkDefaultFont", 14)
        )
        basic_radio.grid(row=0, column=0, padx=(0, 20))

        adaptive_radio = tk.Radiobutton(
            radio_frame,
            text="AdaptiveLns",
            variable=self.algorithm_var,
            value="AdaptiveLns",
            font=("TkDefaultFont", 14)
        )
        adaptive_radio.grid(row=0, column=1)

        self.algorithm_var.trace_add("write", self.on_algorithm_selected)


        destroy_label_font = ("TkDefaultFont", 16)
        destroy_font = ("TkDefaultFont", 14)

        destroy_label = tk.Label(
            top_frame,
            text="Destroy Heuristic:",
            font=destroy_label_font
        )
        destroy_label.grid(row=4, column=0, sticky="w", pady=(20, 4))

        destroy_frame = tk.Frame(top_frame)
        destroy_frame.grid(row=5, column=0, sticky="ew", pady=(0, 12))
        for i in range(4):
            destroy_frame.grid_columnconfigure(i, weight=1)

        destroy_names = ["RandomDestroy", "WorstDestroy", "RelatedDestroy", "WorstRouteDestroy"]
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
            text="Repair Heuristic:",
            font=repair_label_font
        )
        repair_label.grid(row=6, column=0, sticky="w", pady=(20, 4))

        repair_frame = tk.Frame(top_frame)
        repair_frame.grid(row=7, column=0, sticky="ew", pady=(0, 12))

        for i in range(2):
            repair_frame.grid_columnconfigure(i, weight=1)

        repair_names = ["GreedyRepair", "RegretRepair"]
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
            text="Number of iterations:",
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
            text="Run",
            command=self.run_algorithm,
            font=("TkDefaultFont", 14),
            width=10,
        )
        run_button.grid(row=10, column=0, sticky="e", pady=(10, 0))

    def run_app(self):
        self.root.mainloop()
