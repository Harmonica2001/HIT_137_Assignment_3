import tkinter as tk
from tkinter import ttk, filedialog


class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter AI GUI")
        self.geometry("900x700")

        # Create menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Load Model")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

        # ---------------- Model Selection Section ----------------
        model_frame = ttk.LabelFrame(self, text="Model Selection")
        model_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(model_frame, text="Select Model:").pack(side="left", padx=5, pady=5)
        self.model_choice = tk.StringVar()
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_choice,
                                      values=["Text-to-Image", "Image Classification", "Text Generation"],
                                      state="readonly", width=30)
        model_dropdown.pack(side="left", padx=5, pady=5)

        ttk.Button(model_frame, text="Load Model").pack(side="left", padx=5, pady=5)

        # ---------------- User Input Section ----------------
        input_frame = ttk.LabelFrame(self, text="User Input Section")
        input_frame.pack(fill="x", padx=10, pady=5)

        self.input_type = tk.StringVar(value="Text")
        ttk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text").pack(side="left", padx=5)
        ttk.Radiobutton(input_frame, text="Image", variable=self.input_type, value="Image").pack(side="left", padx=5)

        ttk.Button(input_frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)

        self.input_entry = tk.Text(input_frame, height=5, width=60)
        self.input_entry.pack(padx=10, pady=10, fill="x")

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Run Model 1").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Run Model 2").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_input).pack(side="left", padx=5)

        # ---------------- Output Section ----------------
        output_frame = ttk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="both", padx=10, pady=5, expand=True)

        ttk.Label(output_frame, text="Output Display:").pack(anchor="w", padx=5, pady=5)
        self.output_box = tk.Text(output_frame, wrap="word", height=10)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=5)

        # ---------------- Model Info & Explanations ----------------
        info_explain_frame = ttk.LabelFrame(self, text="Model Information & Explanation")
        info_explain_frame.pack(fill="both", padx=10, pady=5, expand=True)

        # Left: Model Info
        model_info_frame = ttk.Frame(info_explain_frame)
        model_info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(model_info_frame, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.model_info_box = tk.Text(model_info_frame, wrap="word", height=10)
        self.model_info_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Right: OOP Explanations
        explain_frame = ttk.Frame(info_explain_frame)
        explain_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(explain_frame, text="OOP Concepts Explanation:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.explain_box = tk.Text(explain_frame, wrap="word", height=10)
        self.explain_box.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------------- Notes Section ----------------
        notes_frame = ttk.LabelFrame(self, text="Notes")
        notes_frame.pack(fill="x", padx=10, pady=5)

        self.notes_box = tk.Text(notes_frame, wrap="word", height=3)
        self.notes_box.pack(fill="x", padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            self.input_entry.delete("1.0", tk.END)
            self.input_entry.insert(tk.END, file_path)

    def clear_input(self):
        self.input_entry.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)


if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
